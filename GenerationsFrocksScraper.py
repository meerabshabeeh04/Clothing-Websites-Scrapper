import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Create a folder to save the images
if not os.path.exists('generation_images'):
    os.makedirs('generation_images')

# Initialize the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless if you don't want to open the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the website
url = "https://generation.com.pk/search?page=1&q=frocks&type=product"
driver.get(url)

# Scroll the page in intervals to ensure all images are loaded
scroll_pause_time = 2  # Wait time between scrolls
scroll_amount = 800  # Number of pixels to scroll by each time

# Scroll down in steps to trigger lazy loading
while True:
    # Scroll by a certain amount
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    
    # Wait for images to load
    time.sleep(scroll_pause_time)
    
    # Check if reached the bottom of the page
    current_scroll_position = driver.execute_script("return window.scrollY + window.innerHeight")
    total_page_height = driver.execute_script("return document.body.scrollHeight")
    
    if current_scroll_position >= total_page_height:
        break

# Allow some extra time for any remaining images to load
time.sleep(5)

# Locate all product elements by their class
product_items = driver.find_elements(By.CLASS_NAME, 'ProductItem__Wrapper')

# Iterate over each product and download the images
image_count = 0
skipped_count = 0
for item in product_items:
    try:
        # Find the img tag within the product item
        img_element = item.find_element(By.TAG_NAME, 'img')
        
        # Check for data-srcset or fallback to src attribute (for lazy-loaded images)
        img_url = img_element.get_attribute('data-srcset')
        if not img_url:
            img_url = img_element.get_attribute('src')
        
        # Ensure the URL is valid and starts with "https:"
        if img_url and 'svg' not in img_url:  # Skip non-product images like SVGs (e.g., phone logo)
            img_url = img_url.split(', ')[-1].split(' ')[0]  # Get the largest image URL
            if not img_url.startswith('https:'):
                img_url = "https:" + img_url

            # Create a valid filename
            img_name = img_url.split('/')[-1].split('?')[0]

            # Download the image
            img_data = requests.get(img_url).content
            with open(f'generation_images/{img_name}', 'wb') as handler:
                handler.write(img_data)
            image_count += 1
            print(f'Downloaded {img_name}')
        else:
            skipped_count += 1
            print(f"No valid image URL found or non-product image, skipping... ({skipped_count})")
    except Exception as e:
        print(f"Error processing image: {e}")

# Close the browser
driver.quit()

print(f'Total images downloaded: {image_count}')
print(f'Total products skipped: {skipped_count}')
