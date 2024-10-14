import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Create a folder to save the images
save_folder = 'lulusar_images'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Function to scrape images from a single page
def scrape_images_from_page(url, start_count):
    driver.get(url)
    
    # Get all divs with the class 'media media--transparent media--hover-effect'
    image_divs = driver.find_elements(By.CSS_SELECTOR, "div.media.media--transparent.media--hover-effect img")
    
    # Extract image URLs and download them starting from start_count
    for index, img in enumerate(image_divs, start=start_count):
        srcset = img.get_attribute('srcset')
        # Get the largest image from srcset
        if srcset:
            # Split the srcset string by commas, pick the last URL (largest image)
            img_url = srcset.split(",")[-1].split()[0]
            img_url = urljoin(url, img_url)  # Make sure it's a full URL
            
            # Download the image
            img_data = requests.get(img_url).content
            img_name = os.path.join(save_folder, f'image_{index}.jpg')
            
            with open(img_name, 'wb') as handler:
                handler.write(img_data)
                print(f"Downloaded {img_name}")
                
    # Return the next starting count after the last image
    return start_count + len(image_divs)

# Main function to scrape multiple pages
def scrape_images_from_multiple_pages(page_links, start_count):
    for page_url in page_links:
        print(f"Scraping images from: {page_url}")
        start_count = scrape_images_from_page(page_url, start_count)
    print("Scraping completed!")

# Modify this list to include all the page URLs you want to scrape
page_links = [
    "https://www.lulusar.com/collections/dresses?page=3",
    "https://www.lulusar.com/collections/dresses?page=4",
    "https://www.lulusar.com/collections/dresses?page=5",
    "https://www.lulusar.com/collections/dresses?page=6",
    "https://www.lulusar.com/collections/dresses?page=7",
    "https://www.lulusar.com/collections/dresses?page=8",
    "https://www.lulusar.com/collections/dresses?page=9",
    "https://www.lulusar.com/collections/dresses?page=10",
    "https://www.lulusar.com/collections/dresses?page=11",
    "https://www.lulusar.com/collections/dresses?page=12",
    "https://www.lulusar.com/collections/dresses?page=13",
    "https://www.lulusar.com/collections/dresses?page=14",
    "https://www.lulusar.com/collections/dresses?page=15",
    "https://www.lulusar.com/collections/dresses?page=16",
    "https://www.lulusar.com/collections/dresses?page=17",
    "https://www.lulusar.com/collections/dresses?page=18",
    # Add more page links here
]

# Set the starting image number
start_image_count = 97  # You can change this if needed

# Call the main function to scrape from all the pages
scrape_images_from_multiple_pages(page_links, start_image_count)

# Close the WebDriver
driver.quit()
