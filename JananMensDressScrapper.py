import httpx
from bs4 import BeautifulSoup

# 1. Find image links on the website
image_links = []
scrapping_links = ["https://janan.com/collections/shalwar-kameez","https://janan.com/collections/shalwar-kameez?page=2","https://janan.com/collections/shalwar-kameez?page=3","https://janan.com/collections/shalwar-kameez?page=4","https://janan.com/collections/shalwar-kameez?page=5","https://janan.com/collections/shalwar-kameez?page=6","https://janan.com/collections/shalwar-kameez?page=7","https://janan.com/collections/shalwar-kameez?page=8","https://janan.com/collections/shalwar-kameez?page=9","https://janan.com/collections/shalwar-kameez?page=10","https://janan.com/collections/shalwar-kameez?page=11","https://janan.com/collections/shalwar-kameez?page=12","https://janan.com/collections/shalwar-kameez?page=13","https://janan.com/collections/shalwar-kameez?page=14","https://janan.com/collections/shalwar-kameez?page=15","https://janan.com/collections/shalwar-kameez?page=16","https://janan.com/collections/shalwar-kameez?page=17","https://janan.com/collections/shalwar-kameez?page=18","https://janan.com/collections/shalwar-kameez?page=19","https://janan.com/collections/shalwar-kameez?page=20","https://janan.com/collections/shalwar-kameez?page=21"]
for url in scrapping_links:
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for image_box in soup.select("div.grid-product__content"):
        page_url = "https://janan.com/" + image_box.select_one("a").attrs["href"]
        print(page_url)
        page_response = httpx.get(page_url, timeout=100.0)
        page_soup = BeautifulSoup(page_response.text, "html.parser")
        wrapper = page_soup.select_one("div.product__thumbs--scroller")
        for image in wrapper.select("img"):
            if 'data-src' in image.attrs:
                result = image.attrs["data-src"]
            else:
                result = image.attrs["src"]
            # result = image.attrs["data-src"]
            # # Append each image and title to the result array
            link = "https:" + str(result)
            image_links.append(link)
print(image_links)

# 2. Download image objects
skip = 0
count = 5647
for image_object in image_links:
    # Create a new .png image file
    if skip % 2 != 0:
        with open(f"./images/image{str(count)}.png", "wb") as file:
            image = httpx.get(image_object, timeout=500.0)
            # Save the image binary data into the file
            file.write(image.content)
            print(f"Image {str(count)} has been scraped")
            count += 1
    skip += 1