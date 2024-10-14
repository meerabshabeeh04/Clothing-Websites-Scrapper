import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def clean_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create a directory to save images
output_folder = 'scraped_images'
os.makedirs(output_folder, exist_ok=True)

# List of URLs to scrape
urls = [
    'https://tehwaarofficial.com/search?options%5Bprefix%5D=last&page=1&q=frocks',
    'https://tehwaarofficial.com/search?options%5Bprefix%5D=last&page=2&q=frocks',
    'https://tehwaarofficial.com/search?options%5Bprefix%5D=last&page=3&q=frocks',
    'https://tehwaarofficial.com/search?options%5Bprefix%5D=last&page=4&q=frocks',
    'https://tehwaarofficial.com/search?options%5Bprefix%5D=last&page=5&q=frocks',
    'https://tehwaarofficial.com/search?options%5Bprefix%5D=last&page=6&q=frocks',
    'https://tehwaarofficial.com/search?options%5Bprefix%5D=last&page=7&q=frocks',
    'https://tehwaarofficial.com/search?options%5Bprefix%5D=last&page=8&q=frocks'
    # Add more URLs here
]

# Counter for image naming
image_counter = 1

# Loop through each URL
for url in urls:
    driver.get(url)

    # Find all image elements
    image_elements = driver.find_elements(By.CSS_SELECTOR, 'div.card__media img')

    # Loop through each image element and download the images
    for img in image_elements:
        img_url = img.get_attribute('src')
        
        # Create the new image name based on the counter
        img_name = f'image_{image_counter}.jpg'
        img_path = os.path.join(output_folder, img_name)

        # Download the image
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded: {img_name}')
            image_counter += 1  # Increment the counter for the next image
        else:
            print(f'Failed to download: {img_url}')

# Close the driver
driver.quit()
