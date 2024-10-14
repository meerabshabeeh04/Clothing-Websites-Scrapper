import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the directory to save images
save_directory = 'fairy_gowns_images'
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no browser UI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the target webpage
url = 'https://www.fairytale.pk/collections/fairy-gowns?page=3'
driver.get(url)
time.sleep(5)  # Wait for the page to load

# Scroll to the bottom of the page to load all images
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Find all image elements within the div with class 'product-card__figure'
image_elements = driver.find_elements(By.CSS_SELECTOR, 'div.product-card__figure img')

# Function to download and save images
def download_image(image_url, image_name):
    try:
        image_data = requests.get(image_url).content
        with open(os.path.join(save_directory, image_name), 'wb') as image_file:
            image_file.write(image_data)
            print(f"Downloaded {image_name}")
    except Exception as e:
        print(f"Failed to download {image_name}: {e}")

# Ask the user for the starting image number
start_image_number = 96

# Iterate over found images and download them
for i, image_element in enumerate(image_elements):
    image_url = image_element.get_attribute('src')
    if image_url.startswith('//'):
        image_url = 'https:' + image_url  # Ensure URL is correct
    image_name = f'image_{start_image_number + i}.jpg'
    download_image(image_url, image_name)

# Close the browser
driver.quit()

print("Scraping completed.")
