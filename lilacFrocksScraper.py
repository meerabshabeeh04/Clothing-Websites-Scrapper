import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the folder to save images
save_folder = 'scraped_images'
os.makedirs(save_folder, exist_ok=True)

# Initialize the webdriver using ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the website to scrape
url = 'https://lylacbymaheen.co/collections/long-dress?page=7'
driver.get(url)

# Wait for images to load
time.sleep(5)  # Adjust if necessary

# Find all image containers
image_divs = driver.find_elements(By.CSS_SELECTOR, '.t4s-product-img')

# Initialize a counter for image names
image_counter = 73

# Loop through each image div and save the images
for div in image_divs:
    # Get the main image source
    img = div.find_element(By.CSS_SELECTOR, '.t4s-product-main-img')
    img_src = img.get_attribute('data-srcset').split(',')[0].split(' ')[0]
    
    # Check if the img_src starts with '//', then prepend 'https:' 
    if img_src.startswith('//'):
        img_src = 'https:' + img_src

    # Download and save the image
    img_data = requests.get(img_src).content
    with open(os.path.join(save_folder, f'image_{image_counter}.jpg'), 'wb') as f:
        f.write(img_data)
    
    print(f'Saved image_{image_counter}.jpg')
    image_counter += 1

# Close the webdriver
driver.quit()
