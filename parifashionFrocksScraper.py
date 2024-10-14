import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the download folder
download_folder = 'parifashion_images'
os.makedirs(download_folder, exist_ok=True)

# Set the starting index for naming images
starting_index = 95  # Change this to the desired starting index

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no GUI)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Function to download images
def download_image(url, index, folder):
    try:
        # Add 'https:' to the URL if it starts with '//'
        if url.startswith('//'):
            url = 'https:' + url
        
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Create a valid filename with the specified index
            filename = os.path.join(folder, f'image_{index}.jpg')
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded: {filename}')
        else:
            print(f'Failed to retrieve image from {url}')
    except Exception as e:
        print(f'Error downloading {url}: {e}')

# URL to scrape
url = 'https://parifashion.com.pk/search?q=maxi*&type=product'
driver.get(url)

# Scroll to the bottom to load all images
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the page to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # Break the loop if no new content is loaded
    if new_height == last_height:
        break
    last_height = new_height

# Allow a final wait to ensure all lazy-loaded images are displayed
time.sleep(2)

# Locate the image containers
image_divs = driver.find_elements(By.CSS_SELECTOR, 'div.AspectRatio.AspectRatio--withFallback')

# Extract image URLs and download them
image_count = starting_index
for div in image_divs:
    img_tags = div.find_elements(By.TAG_NAME, 'img')
    for img in img_tags:
        img_url = None
        
        # Check if data-srcset is present and valid
        data_srcset = img.get_attribute('data-srcset')
        if data_srcset:
            img_url = data_srcset.split(',')[0].split(' ')[0]  # Get the first image URL
        else:
            # Fallback to the src attribute if data-srcset is not present
            img_url = img.get_attribute('src')
        
        # Check if img_url is valid
        if img_url:
            download_image(img_url, image_count, download_folder)
            image_count += 1  # Increment the index for the next image
        else:
            print('No valid image URL found for this image.')

# Close the WebDriver
driver.quit()






