import httpx
from bs4 import BeautifulSoup

# 1. Find image links on the website
image_links = []
scrapping_links = ["https://www.limelight.pk/collections/men-kurta","https://www.limelight.pk/collections/men-suits"]
for url in scrapping_links:
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for image_box in soup.select("li.grid__item"):
        page_url = "https://www.limelight.pk"+image_box.select_one("a").attrs["href"]
        print(page_url)
        page_response = httpx.get(page_url, timeout=30.0)
        page_soup = BeautifulSoup(page_response.text, "html.parser")
        wrapper = page_soup.select_one("div.product-secondary-imgs")
        for image in wrapper.select("img"):
            result = image.attrs["src"]
            # Append each image and title to the result array
            link = "https:"+str(result)
            image_links.append(link)
print(image_links)

# 2. Download image objects
count = 2255
for image_object in image_links:
    # Create a new .png image file
    with open(f"./images/image{str(count)}.png", "wb") as file:
        image = httpx.get(image_object, timeout=30.0)
        # Save the image binary data into the file
        file.write(image.content)
        print(f"Image {str(count)} has been scraped")
        count += 1