import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Ask user for the starting image number
start_number = 174

# Folder where images will be saved
folder_name = "scraped_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Set up the Chrome WebDriver using the ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
url = "https://www.stylebyrk.com/collections/gown"
driver.get(url)

# Scroll to the bottom to load all images (adjust the scrolling mechanism if necessary)
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the page to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Locate all image divs containing the image data
image_divs = driver.find_elements(By.CLASS_NAME, 'card-media')

# Initialize the image counter
image_counter = start_number

# Loop through each image div and download the image
for div in image_divs:
    try:
        # Find the <img> tag inside the div
        img_tag = div.find_element(By.TAG_NAME, 'img')

        # Get the high-resolution image URL from the 'data-srcset' attribute
        img_url = img_tag.get_attribute('data-srcset').split(",")[-1].split(" ")[0]

        # Download the image
        img_data = requests.get("https:" + img_url).content

        # Save the image in the specified folder with the incremented image counter
        image_path = os.path.join(folder_name, f"image_{image_counter}.jpg")
        with open(image_path, 'wb') as handler:
            handler.write(img_data)

        print(f"Downloaded image {image_counter}: {img_url}")

        # Increment the image counter
        image_counter += 1

    except Exception as e:
        print(f"Failed to download image: {e}")

# Close the browser
driver.quit()
