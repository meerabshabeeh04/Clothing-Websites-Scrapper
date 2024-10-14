import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL to scrape
url = 'https://www.zeekstore.com/collections/maxis?page=2'
driver.get(url)

# Scroll to load lazy-loaded images
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the page to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Create a folder to save the images
output_folder = 'zeekstore_images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Ask for the starting index for image numbering
starting_index = 81

# Find all image elements inside <div> with class 'reveal'
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.reveal img")

# Download and save the images
for idx, img in enumerate(image_elements):
    img_url = img.get_attribute("data-original")
    if not img_url:
        continue
    img_url = "https:" + img_url  # Ensure full URL
    img_data = requests.get(img_url).content
    image_number = starting_index + idx
    with open(f"{output_folder}/image_{image_number}.jpg", "wb") as handler:
        handler.write(img_data)
    print(f"Saved: image_{image_number}.jpg")

# Close the WebDriver
driver.quit()

