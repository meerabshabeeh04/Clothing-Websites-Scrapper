import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options (you can add more options if needed)
chrome_options = webdriver.ChromeOptions()

# Initialize the WebDriver using ChromeDriverManager and Service
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL of the page to scrape
url = 'https://lamisfashion.pk/product-category/maxi-dresses/'

# Create a folder to save the images
folder_name = 'lamisfashion_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Start an index for the image filenames
image_index = 1

# Open the webpage
driver.get(url)

# Scroll the page in intervals to trigger lazy loading (adjust if needed)
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    
    # Check if the page has finished loading
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all div elements with the class 'hover-img'
image_divs = driver.find_elements(By.CLASS_NAME, 'hover-img')

# Loop through all found divs and download the images
for div in image_divs:
    try:
        # Find the img tag inside the div
        img_tag = div.find_element(By.TAG_NAME, 'img')
        img_url = img_tag.get_attribute('src')  # Get the image URL
        
        # Download and save the image
        img_data = requests.get(img_url).content
        img_filename = f'image_{image_index}.jpg'
        with open(os.path.join(folder_name, img_filename), 'wb') as img_file:
            img_file.write(img_data)
        
        print(f'Downloaded {img_filename}')
        image_index += 1  # Increment the image index
    except Exception as e:
        print(f"Failed to download an image: {e}")

# Close the browser
driver.quit()

