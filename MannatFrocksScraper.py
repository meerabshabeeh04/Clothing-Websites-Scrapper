from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import os

# Set up the Chrome WebDriver using webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# List of URLs to scrape from
urls = [
    "https://mannatclothing.com/search?options%5Bprefix%5D=last&page=1&q=frock",
    "https://mannatclothing.com/search?options%5Bprefix%5D=last&page=2&q=frock",
    "https://mannatclothing.com/search?options%5Bprefix%5D=last&page=3&q=frock",
    "https://mannatclothing.com/search?options%5Bprefix%5D=last&page=4&q=frock",
    "https://mannatclothing.com/search?options%5Bprefix%5D=last&page=5&q=frock",
    "https://mannatclothing.com/search?options%5Bprefix%5D=last&page=6&q=frock",
    "https://mannatclothing.com/search?options%5Bprefix%5D=last&page=7&q=frock"
    # Add more URLs here
]

# Create a directory to save the images
if not os.path.exists('mannat_frock_images'):
    os.makedirs('mannat_frock_images')

# Loop through each URL
for url in urls:
    # Open the webpage
    driver.get(url)

    # Scroll to load images
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find all image elements within the specific div structure
    images = driver.find_elements(By.XPATH, '//div[@class="image-wrap loaded"]//img')

    # Download images
    for index, img in enumerate(images):
        # Get the src attribute from the img tag
        src = img.get_attribute('src')
        if src.startswith('//'):
            src = 'https:' + src

        # Download and save the image with a unique name based on URL and index
        img_path = f'mannat_frock_images/{url.split("page=")[1].split("&")[0]}_image_{index + 1}.jpg'
        urllib.request.urlretrieve(src, img_path)
        print(f"Downloaded: {img_path}")

# Close the browser
driver.quit()
