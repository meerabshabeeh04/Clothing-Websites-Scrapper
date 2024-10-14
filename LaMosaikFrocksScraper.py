import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Set up the folder to save images
folder_name = "lamosaik_maxi_dress_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Specify the starting number for image filenames
start_index = 176

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# List of URLs to scrape
urls = [
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=9&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=10&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=11&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=12&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=13&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=14&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=15&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=16&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=17&q=frocks%2A&type=product",
    "https://lamosaik.com/search?options%5Bprefix%5D=none&options%5Bunavailable_products%5D=last&page=18&q=frocks%2A&type=product",
]

# Initialize the global image counter with the provided start_index
image_counter = start_index

# Loop through each URL in the list
for url in urls:
    print(f"Scraping images from {url}")
    
    # Open the page
    driver.get(url)

    # Scroll down to load all images (adjust range and time.sleep as needed)
    for _ in range(10):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

    # Give time for all lazy-loaded images to be fully loaded
    time.sleep(5)

    # Find all divs with the class that contains background images
    divs = driver.find_elements(By.CSS_SELECTOR, "div.pr_lazy_img.main-img.nt_img_ratio.nt_bg_lz")

    # Loop through the divs to extract and download images
    for div in divs:
        try:
            # Extract the image URL from the style attribute (background-image)
            style_attribute = div.get_attribute("style")
            if "background-image" in style_attribute:
                # Extract URL from background-image: url(...)
                start = style_attribute.find('url("') + len('url("')
                end = style_attribute.find('")', start)
                image_url = style_attribute[start:end]

                # Ensure the full URL is constructed
                if image_url.startswith("//"):
                    image_url = "https:" + image_url

                # Download the image and save it
                img_data = requests.get(image_url).content
                img_name = f"{folder_name}/image_{image_counter}.jpg"  # Use global image_counter
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded: {img_name}")
                
                # Increment the global image counter
                image_counter += 1
            else:
                print(f"No background image found for image {image_counter}")

        except Exception as e:
            print(f"Error downloading image {image_counter}: {e}")

# Close the browser
driver.quit()
