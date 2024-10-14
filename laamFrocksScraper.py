from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

# Scrape the webpage
#https://laam.pk/nodes/women-angrakha-187
#https://laam.pk/nodes/women-maxi-299
scrapping_links = ["https://laam.pk/nodes/women-angrakha-187"]

image_links = []

for url in scrapping_links:
    driver.get(url)
    # Wait for the page to fully load (you can adjust the sleep time or use WebDriverWait)
    time.sleep(200)  # Or use WebDriverWait for better handling

    # Get the page source and parse it using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Select the div containing the images
    for image_box in soup.select("div.product_card.flex.flex-col"):
        print("Div Found!")
        img_tag = image_box.find("img")
        if img_tag and img_tag.get("src"):
            print('Img Found')
            result = img_tag["src"]
            image_links.append(result)
        else:
            print('Img Not Found')

print(image_links)

# Close the Selenium WebDriver
driver.quit()

# 2. Download image objects
import httpx
#326angrakha
count = 326
timeout = httpx.Timeout(500.0) 
for image_object in image_links:
    with open(f"./images/image{str(count)}.png", "wb") as file:
        image = httpx.get(image_object)
        file.write(image.content)
        print(f"Image {str(count)} has been scraped")
        count += 1