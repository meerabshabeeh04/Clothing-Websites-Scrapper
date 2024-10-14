from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
url = 'https://www.lalazarshop.com/search?q=frock*&type=product'
driver.get(url)

# Scroll down to load more products (Adjust based on the page structure)
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Scraping the product images
product_images = driver.find_elements(By.CSS_SELECTOR, '.ProductItem__ImageWrapper img')

# Create a directory to save the images
if not os.path.exists('lalazar_images'):
    os.mkdir('lalazar_images')

# Download the images
for idx, img in enumerate(product_images):
    img_url = img.get_attribute('data-srcset')
    
    # Debugging: Print the raw img_url
    print(f"Raw data-srcset for image {idx+1}: {img_url}")

    # Extract the highest resolution image from the srcset attribute
    if img_url:
        try:
            # Split the srcset into a list of URLs and resolutions
            url_entries = img_url.split(',')
            # Get the URL with the highest resolution (typically the last one)
            highest_res_entry = url_entries[-1].strip().split(' ')[0]

            # Ensure URL is complete
            if highest_res_entry.startswith('//'):
                highest_res_entry = 'https:' + highest_res_entry  # Prepend https: to relative URL
            elif not highest_res_entry.startswith('http'):
                print(f"Invalid URL skipped: {highest_res_entry}")
                continue  # Skip invalid URLs

            # Download and save the image
            img_data = requests.get(highest_res_entry).content
            img_name = f'lalazar_images/image_{idx+1}.jpg'
            with open(img_name, 'wb') as handler:
                handler.write(img_data)
            print(f'Downloaded: {img_name}')
        except Exception as e:
            print(f"Error downloading {highest_res_entry}: {e}")

# Close the driver
driver.quit()





