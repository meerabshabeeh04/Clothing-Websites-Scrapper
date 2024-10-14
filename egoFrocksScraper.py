import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from urllib.parse import urljoin

folder_name = "wearego_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the website
url = "https://wearego.com/search?filter.v.option.size=XS&filter.v.option.size=S&filter.v.option.size=M&filter.v.option.size=L&filter.v.option.size=XL&q=frock&view=&filter.v.availability=1"
driver.get(url)

# Scroll and wait for elements to load dynamically
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for new images to load
    time.sleep(scroll_pause_time)
    
    # Wait for divs containing images to load using WebDriverWait
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.gitem-img.primary.lazyloaded")))

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Allow some time for all images to finish loading after scrolling
time.sleep(5)

# Find all divs with class 'gitem-img primary lazyloaded'
divs = driver.find_elements(By.CSS_SELECTOR, "div.gitem-img.primary.lazyloaded")

# Track downloaded image URLs to avoid duplicates
downloaded_urls = set()

# Loop through each div and extract image URL from 'data-bgset'
for index, div in enumerate(divs):
    data_bgset = div.get_attribute('data-bgset')
    if data_bgset:
        # Extract the largest image URL from data-bgset (last one)
        image_urls = data_bgset.split(',')
        largest_image_url = image_urls[-1].split(' ')[0]
        full_image_url = urljoin(url, largest_image_url)

        # Only download if the image hasn't been downloaded before
        if full_image_url not in downloaded_urls:
            downloaded_urls.add(full_image_url)

            # Download the image and save it
            image_data = requests.get(full_image_url).content
            image_name = f"image_{index+1}.jpg"
            with open(os.path.join(folder_name, image_name), 'wb') as f:
                f.write(image_data)
            print(f"Downloaded {image_name}")

# Close the driver
driver.quit()


