import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Create a folder to save images
output_folder = 'limelight_images'
os.makedirs(output_folder, exist_ok=True)

# Start the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# List of URLs to scrape
url_list = [
    "https://www.limelight.pk/collections/dresses"

    # Add more URLs here
    # "https://www.limelight.pk/search?q=frock&page=2",
    # "https://www.limelight.pk/search?q=frock&page=3"
]

# Get the starting image number from the user
starting_image_number = int(input("Enter the starting image number: "))

# Loop through each URL in the list
for url in url_list:
    driver.get(url)
    print(f"Scraping URL: {url}")

    # Allow time for images to load
    time.sleep(5)

    # Find all image elements
    image_elements = driver.find_elements(By.CSS_SELECTOR, "div.media img")

    # Loop through the images and download them
    for index, img in enumerate(image_elements, start=starting_image_number):
        img_url = img.get_attribute('src')
        if img_url:
            # Save the image
            response = requests.get(img_url)
            if response.status_code == 200:
                filename = f'image_{index}.jpg'  # Use the specified starting number
                with open(os.path.join(output_folder, filename), 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download image {index}: {response.status_code}")

# Close the driver
driver.quit()
