#Worked
import httpx
from bs4 import BeautifulSoup
import os

# 1. Find image links on the website
image_links = []
base_url = "https:"  # Define the base URL
scrapping_links = ["https://www.shopmanto.com/collections/anarkali"]
# Scrape the first 4 pages
for url in scrapping_links:
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for image_box in soup.select("div.product-item__inner"):
        result = image_box.select_one("img").attrs["src"]
        # Append the full URL (base URL + relative path) to the image_links array
        full_url = base_url + result
        image_links.append(full_url)

print(image_links)

# 2. Download image objects
if not os.path.exists('./images'):
    os.makedirs('./images')

count = 0
for image_object in image_links:
    # Create a new .png image file
    with open(f"./images/image{str(count)}.png", "wb") as file:
        image = httpx.get(image_object)
        # Save the image binary data into the file
        file.write(image.content)
        print(f"Image {str(count)} has been scraped")
        count += 1
