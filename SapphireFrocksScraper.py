#Worked

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import httpx
import os

# Ensure the 'images' directory exists
os.makedirs('./images', exist_ok=True)

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode (without GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the target page
scraping_url = "https://pk.sapphireonline.pk/pages/search-results-page?q=maxi&tab=products&page=2"
driver.get(scraping_url)

# Wait for the page to fully load and images to be present (optional but can help with timing)
driver.implicitly_wait(10)

# 1. Find image links on the website
image_links = []
# Find image elements using the appropriate CSS selector
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.snize-thumbnail-wrapper img.snize-item-image")

for img in image_elements:
    # Extract the image src attribute
    src = img.get_attribute("src")
    if src:
        image_links.append(src)

print(f"Found {len(image_links)} images.")

# Close the Selenium WebDriver
driver.quit()

# 2. Download image objects
count = 0
for image_object in image_links:
    try:
        # Create a new .jpg image file
        with open(f"./images/image{str(count)}.jpg", "wb") as file:
            image = httpx.get(image_object)
            # Save the image binary data into the file
            file.write(image.content)
            print(f"Image {str(count)} has been scraped")
            count += 1
    except Exception as e:
        print(f"Failed to scrape image {count}: {e}")



'''
<div class="snize-thumbnail-wrapper">
<span class="snize-thumbnail">
<img src="https://cdn.shopify.com/s/files/1/1592/0041/files/WESTTOP03414_1_large.jpg?v=1719584031" class="snize-item-image " alt="Women's Western Wear Yellow Dress" border="0" loading="lazy">
<img src="https://cdn.shopify.com/s/files/1/1592/0041/files/WESTTOP03414_2_large.jpg?v=1719584031" alt="Women's Western Wear Yellow Dress" class="snize-item-image snize-flip-image " border="0" loading="lazy">
</span>
</div>
'''