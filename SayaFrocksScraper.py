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
scraping_url = "https://saya.pk/search?type=product&options%5Bunavailable_products%5D=last&options%5Bprefix%5D=last&q=frock"
driver.get(scraping_url)

# Wait for the page to fully load and images to be present (optional but can help with timing)
driver.implicitly_wait(10)

# 1. Find image links on the website
image_links = []
# Find image elements using the appropriate CSS selector
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.t4s-product-img img.t4s-product-main-img")

for img in image_elements:
    # Extract the image srcset or src attribute
    srcset = img.get_attribute("data-srcset")
    if srcset:
        result = srcset.split(",")[-1].split()[0]  # Get the highest resolution image link
        if result.startswith("//"):
            result = "https:" + result
        image_links.append(result)

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


