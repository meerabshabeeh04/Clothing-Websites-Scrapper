import httpx
from bs4 import BeautifulSoup

# 1. Find image links on the website
image_links = []
scrapping_links = ["https://pk.sapphireonline.pk/collections/man-stitched-fall-winter-24","https://pk.sapphireonline.pk/collections/man-stitched-festive-24","https://pk.sapphireonline.pk/collections/kurtas","https://pk.sapphireonline.pk/collections/kurtas?page=2","https://pk.sapphireonline.pk/collections/kurta-shalwar","https://pk.sapphireonline.pk/collections/kurta-shalwar?page=2"]
for url in scrapping_links:
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for image_box in soup.select("div.t4s-product"):
        page_url = "https://pk.sapphireonline.pk/"+image_box.select_one("a").attrs["href"]
        print(page_url)
        page_response = httpx.get(page_url, timeout=30.0)
        page_soup = BeautifulSoup(page_response.text, "html.parser")
        wrapper = page_soup.select_one("div.t4s-col-12.t4s-col-item.t4s-pr")
        for image in wrapper.select("img"):
            result = image.attrs["src"]
            # Append each image and title to the result array
            link = "https:"+str(result)
            image_links.append(link)
print(image_links)

# 2. Download image objects
count = 4115
skip = 0
for image_object in image_links:
    if skip%2==0:
    # Create a new .png image file
        with open(f"./images/image{str(count)}.png", "wb") as file:
            image = httpx.get(image_object, timeout=100.0)
            # Save the image binary data into the file
            file.write(image.content)
            print(f"Image {str(count)} has been scraped")
            count += 1
    skip += 1