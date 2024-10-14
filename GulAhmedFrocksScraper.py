#Worked
import httpx
from bs4 import BeautifulSoup
import os
import mimetypes

# 1. Find image links on the website
image_links = []
scrapping_links = ["https://www.gulahmedshop.com/catalogsearch/result/?q=frock"]

# Scrape the target pages
for url in scrapping_links:
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all divs containing images
    for image_box in soup.select("div.item.main-image"):
        # Look for the img tag inside the <a> tag
        img_tag = image_box.select_one("img")
        
        if img_tag:
            # Try to get the high-quality image from data-owlsrc if available, otherwise use src
            image_url = img_tag.get("data-owlsrc", img_tag.get("src", ""))
            print(f"Found image URL: {image_url}")
            
            # Append the image URL to the list
            image_links.append(image_url)

print(f"Image links found: {image_links}")

# 2. Download image objects
# Create a directory if it doesn't exist
if not os.path.exists('./images'):
    os.makedirs('./images')

count = 0
for image_object in image_links:
    # Make a request to get the image data
    image_response = httpx.get(image_object)
    
    # Get the content type (MIME type) of the image
    content_type = image_response.headers.get("Content-Type", "")
    extension = mimetypes.guess_extension(content_type)  # Guess the file extension based on the content type

    # Default to ".jpg" if the extension is not found
    if not extension:
        extension = ".jpg"
    
    # Save the image with the appropriate file extension
    with open(f"./images/image{str(count)}{extension}", "wb") as file:
        # Save the image binary data into the file
        file.write(image_response.content)
        print(f"Image {str(count)} has been scraped and saved as image{str(count)}{extension}")
        count += 1
