import httpx
from bs4 import BeautifulSoup

# 1. Find image links on the website
image_links = []
# scrapping_links = ["https://bonanzasatrangi.com/collections/kurta-shalwar","https://bonanzasatrangi.com/collections/kurta-shalwar?page=2","https://bonanzasatrangi.com/collections/kurta-shalwar?page=3"]
# scrapping_links = ["https://bonanzasatrangi.com/collections/shalwar-suit","https://bonanzasatrangi.com/collections/shalwar-suit?page=2"]
scrapping_links = ["https://bonanzasatrangi.com/collections/men-blended","https://bonanzasatrangi.com/collections/men-cotton"]
for url in scrapping_links:
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for image_box in soup.select("div.grid-view_image"):
        page_url = "https://bonanzasatrangi.com/"+image_box.select_one("a").attrs["href"]
        print(page_url)
        page_response = httpx.get(page_url, timeout=30.0)
        page_soup = BeautifulSoup(page_response.text, "html.parser")
        wrapper = page_soup.select_one("div.thumbnails-wrapper")
        for image in wrapper.select("img"):
            result = image.attrs["src"]
            # Append each image and title to the result array
            link = "https:"+str(result)
            image_links.append(link)
print(image_links)

# 2. Download image objects
# count = 1989
# count = 2124
count = 2201
for image_object in image_links:
    # Create a new .png image file
    with open(f"./images/image{str(count)}.png", "wb") as file:
        image = httpx.get(image_object)
        # Save the image binary data into the file
        file.write(image.content)
        print(f"Image {str(count)} has been scraped")
        count += 1