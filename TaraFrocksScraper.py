import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# URL of the website to scrape
url = "https://taara.store/collections/dresses"

# Directory to save images
output_folder = "images"
os.makedirs(output_folder, exist_ok=True)

# Initialize the Chrome driver with Service
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

# Optional: Wait for the page to load completely
time.sleep(3)

# Find all image elements in the specified div
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.card-hover-images img")

# Loop through the image elements and download the images
for index, img in enumerate(image_elements):
    img_url = img.get_attribute("src")
    if img_url:
        try:
            # Download and save the image
            img_data = requests.get(img_url).content
            img_file_path = os.path.join(output_folder, f"image_{index + 1}.jpg")
            with open(img_file_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_file_path}")
        except Exception as e:
            print(f"Could not download {img_url}: {e}")

# Close the browser
driver.quit()
