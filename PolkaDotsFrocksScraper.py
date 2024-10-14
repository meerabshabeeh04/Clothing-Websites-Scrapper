import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set the directory where images will be saved
directory = "polkadots_images"
os.makedirs(directory, exist_ok=True)

# Configure your WebDriver
driver = webdriver.Chrome()

# Navigate to the Polkadots page
url = "https://www.polkadots.pk/collections/frocks/?utm_campaign=home&utm_source=frocks&page=3"
driver.get(url)

# Give the page some time to load
time.sleep(5)

# Find all image elements in the frocks collection
image_elements = driver.find_elements(By.CSS_SELECTOR, "img")

# Extract URLs of the images
image_urls = [img.get_attribute('src') for img in image_elements]

# Download the images
for url in image_urls:
    # Extract the filename from the URL
    filename = url.split("/")[-1].split("?")[0]  # This removes the query string
    filepath = os.path.join(directory, filename)

    # Download the image
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filepath}")
    except Exception as e:
        print(f"Could not download {url}: {e}")

# Close the WebDriver
driver.quit()
