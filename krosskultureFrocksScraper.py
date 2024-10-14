import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the folder where images will be saved
folder_path = "kross_kulture_images"
os.makedirs(folder_path, exist_ok=True)

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the target website
url = "https://krosskulture.com/search?q=frocks&options%5Bprefix%5D=last&filter.v.option.size=XS&filter.v.option.size=S&filter.v.option.size=M&filter.v.option.size=L&filter.v.option.size=XL"
driver.get(url)

# Scroll to the bottom of the page to load all images
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for new images to load
    time.sleep(2)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all image elements within the specified div class
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.media.media--transparent.media--hover-effect img")

# Loop through each image element and download the images
for index, img in enumerate(image_elements):
    img_url = img.get_attribute("src")
    
    # Complete the URL if necessary
    if img_url.startswith("//"):
        img_url = "https:" + img_url
    
    # Get the image content
    response = requests.get(img_url)

    # Save the image
    if response.status_code == 200:
        with open(os.path.join(folder_path, f"image_{index + 1}.jpg"), "wb") as file:
            file.write(response.content)
            print(f"Saved image: image_{index + 1}.jpg")
    else:
        print(f"Failed to retrieve image from {img_url}")

# Close the WebDriver
driver.quit()
