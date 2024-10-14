import os
import time
import requests
from PIL import Image  # To handle conversion
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
url = "https://pinkpoppi.com/categorysearch/Frocks"
driver.get(url)
time.sleep(3)  # Allow time for the page to load

# Create a folder to save images
folder_name = "Pinkpoppi_Frocks_Images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Scroll to load more images if necessary (adjust scroll range as needed)
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new content to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find image elements
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.products-pic img")

# Download and convert images
for idx, img in enumerate(image_elements):
    img_url = img.get_attribute("src")
    if img_url:
        img_data = requests.get(img_url).content
        # Convert the image from webp to jpg
        try:
            image = Image.open(BytesIO(img_data)).convert("RGB")
            file_name = os.path.join(folder_name, f"frock_{idx + 1}.jpg")
            image.save(file_name, "JPEG")
            print(f"Downloaded and converted: {file_name}")
        except Exception as e:
            print(f"Failed to convert image {img_url}: {e}")

# Close the driver
driver.quit()
