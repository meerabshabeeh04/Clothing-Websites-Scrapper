from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

# Function to save an image
def save_image(image_url, image_name):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_name, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {image_name}")
        else:
            print(f"Failed to download {image_url}")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

# Main function to scrape images
def scrape_images(start_index=1):
    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://robespk.com/collections/long-dresses?filter.v.price.gte=&filter.v.price.lte=&sort_by=title-descending"
        driver.get(url)
        
        # Wait for the page to load
        time.sleep(5)

        # Find all the divs containing the images
        image_divs = driver.find_elements("css selector", ".card-media.card-media--portrait img")

        # Create a directory to save images
        os.makedirs("images", exist_ok=True)

        for index, img in enumerate(image_divs):
            image_url = img.get_attribute('src')
            if image_url:
                # Create a sequential filename starting from the specified index
                image_name = f"images/image_{start_index + index}.jpg"
                save_image(image_url, image_name)

    finally:
        driver.quit()

# Specify the starting index for images
starting_index = 81  # Change this value as needed
scrape_images(start_index=starting_index)


