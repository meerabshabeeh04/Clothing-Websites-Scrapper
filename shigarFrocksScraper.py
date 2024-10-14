import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set the URL of the page to scrape
url = "https://shigarfashion.com/collections/long-shirts?page=2"

# Create a folder to save the images
folder_name = "shigar_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Set the starting index for image naming
starting_index = 40  # Change this value to set the starting index

# Set up the Selenium WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
driver.get(url)
time.sleep(3)  # Wait for the page to load

# Find all the image elements
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.t4s-product-img img.t4s-product-main-img")

# Loop through the images and download them
for index, img in enumerate(image_elements):
    # Get the image URL from the data-srcset attribute
    img_srcset = img.get_attribute("data-srcset")

    # Check if img_srcset is not None before processing
    if img_srcset:
        img_url = img_srcset.split(",")[0].split(" ")[0]  # Get the first URL from srcset

        # Prepend "https:" to the URL if it's missing
        if img_url.startswith("//"):
            img_url = "https:" + img_url

        img_data = requests.get(img_url).content
        img_name = f"{folder_name}/image_{starting_index + index}.png"  # Use starting index for naming
        with open(img_name, "wb") as img_file:
            img_file.write(img_data)
        print(f"Downloaded: {img_name}")
    else:
        print(f"Image {starting_index + index} has no srcset attribute, skipping.")

# Close the WebDriver
driver.quit()
