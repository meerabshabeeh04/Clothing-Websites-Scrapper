from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Make sure to have the correct driver version
url = 'https://www.kapraymart.com/product-tag/maxi/'
driver.get(url)

# Scroll the page to trigger lazy loading
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Create a folder to save images
folder_name = 'kapraymart_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Find all the divs with class 'image-fade_in_back'
image_divs = driver.find_elements(By.CLASS_NAME, 'image-fade_in_back')

# Counter for naming images
image_counter = 1

for div in image_divs:
    img_tags = div.find_elements(By.TAG_NAME, 'img')
    
    for img in img_tags:
        img_url = img.get_attribute('src')
        
        if img_url:
            # Save image
            img_data = requests.get(img_url).content
            img_name = f'image_{image_counter}.jpg'
            img_path = os.path.join(folder_name, img_name)
            
            with open(img_path, 'wb') as handler:
                handler.write(img_data)
            
            print(f"Downloaded {img_name} from {img_url}")
            image_counter += 1

# Close the browser
driver.quit()
