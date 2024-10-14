import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the WebDriver (Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (optional)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the URL
url = "https://harram.com.pk/product-category/maxi/page/3/"
driver.get(url)
time.sleep(3)  # Wait for the page to load

# Create a folder to save the images
folder_name = "harram_frocks_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Prompt the user to enter the starting image number
start_image_number = 35

# Find all product image containers
product_containers = driver.find_elements(By.CLASS_NAME, "rey-productThumbnail")

# Loop through each container and get the image src
for idx, container in enumerate(product_containers):
    try:
        # Get the image tag inside the container
        img_tag = container.find_element(By.TAG_NAME, "img")
        img_url = img_tag.get_attribute("src")

        # Download the image
        img_data = requests.get(img_url).content
        img_name = f"{folder_name}/image_{start_image_number + idx}.jpeg"
        
        # Save the image
        with open(img_name, "wb") as img_file:
            img_file.write(img_data)
        print(f"Downloaded: {img_name}")

    except Exception as e:
        print(f"Error downloading image {start_image_number + idx}: {e}")

# Close the browser
driver.quit()
