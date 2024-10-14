import httpx
from bs4 import BeautifulSoup

# 1. Find image links on the website
image_links = []
# scrapping_links = ["https://zellbury.com/collections/shalwar-kameez"]
scrapping_links = ["https://zellbury.com/collections/kurta"]
# Scrape the first 4 pages
for url in scrapping_links:
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for image_box in soup.select("div.card__media"):
        # result = image_box.select("img")[1].attrs["src"]
        result = image_box.select_one("img").attrs["src"]
        # Append each image and title to the result array
        link = "https:"+str(result)
        image_links.append(link)
print(image_links)

# 2. Download image objects
count = 1980
for image_object in image_links:
    # Create a new .png image file
    with open(f"./images/image{str(count)}.png", "wb") as file:
        image = httpx.get(image_object)
        # Save the image binary data into the file
        file.write(image.content)
        print(f"Image {str(count)} has been scraped")
        count += 1