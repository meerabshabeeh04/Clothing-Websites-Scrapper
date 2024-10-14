#worked
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import httpx

# Initialize Selenium WebDriver (e.g., using Chrome)
driver = webdriver.Chrome()  # Ensure the correct WebDriver (e.g., chromedriver) is installed

# Target website to scrape
url = "https://nishatlinen.com/search?options%5Bprefix%5D=last&options%5Bunavailable_products%5D=last&page=7&q=long+dresses&type=product"
driver.get(url)

# Scroll and wait for images to load
scroll_pause_time = 3  # Adjust the pause time between scrolls if needed

def scroll_and_load_images(driver, num_scrolls=10):
    image_links = set()
    scroll_height = 1000  # Scroll by this height each time

    for _ in range(num_scrolls):
        # Scroll down by the set amount
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")
        
        # Wait for images to load
        time.sleep(scroll_pause_time)
        
        # Wait explicitly for images to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.t4s-product-img img"))
        )
        
        # Find all images on the page
        images = driver.find_elements(By.CSS_SELECTOR, "div.t4s-product-img img")
        
        # Extract image links from the "data-srcset" attribute
        for img in images:
            srcset = img.get_attribute("data-srcset")
            if srcset:
                # Get the highest resolution image from the srcset
                image_url = srcset.split(",")[-1].split()[0]
                image_links.add(image_url)
                
        # Try clicking 'Load More' if the button exists
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, "button.load-more")
            load_more_button.click()
            time.sleep(scroll_pause_time)  # Wait for more images to load
        except:
            # No 'Load More' button found
            pass

    return list(image_links)

# Call the function to scroll and load images
image_links = scroll_and_load_images(driver, num_scrolls=15)

# Close the WebDriver
driver.quit()

# Print the number of images scraped
print(f"Found {len(image_links)} images.")

# Create the directory to save images if it doesn't exist
os.makedirs("./images", exist_ok=True)

# Download the images
count = 0
for image_url in image_links:
    try:
        image_data = httpx.get("https:" + image_url)
        with open(f"./images/image{count}.jpg", "wb") as file:
            file.write(image_data.content)
            print(f"Image {count} has been scraped")
        count += 1
    except Exception as e:
        print(f"Failed to download image {image_url}: {e}")
