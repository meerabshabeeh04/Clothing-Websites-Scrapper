import httpx
from bs4 import BeautifulSoup
import os

# 1. Define the website URL
scrapping_links = ["https://hussnaindesigner.com/"]

# 2. Create a list to store image links
image_links = []

# 3. Scrape the pages
for url in scrapping_links:
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Select the div with class 'card__media' and look for images inside
    for image_box in soup.select("div.card__media img"):
        # Extract the 'srcset' attribute for high-resolution images
        srcset = image_box.get("srcset")
        if srcset:
            # Get the highest resolution image from the srcset
            image_url = srcset.split(",")[-1].split()[0]
            image_links.append(image_url)
        else:
            # If 'srcset' is not available, fall back to 'src'
            image_links.append(image_box.get("src"))
            
# Print the number of images found
print(f"Found {len(image_links)} images.")
print(image_links)

# 4. Create a directory to save the images if it doesn't exist
os.makedirs("./images", exist_ok=True)

# 5. Download the images
count = 0
for image_object in image_links:
    try:
        # Prepend "https:" to the image URL if not already included
        if not image_object.startswith("http"):
            image_object = "https:" + image_object
            
        # Download the image
        image_data = httpx.get(image_object)
        
        # Save the image to the local directory as .jpg
        with open(f"./images/image{str(count)}.jpg", "wb") as file:
            file.write(image_data.content)
            print(f"Image {str(count)} has been scraped")
        
        count += 1
    except Exception as e:
        print(f"Failed to download image {image_object}: {e}")
