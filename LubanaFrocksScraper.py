from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time

# Set up the webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless browser to avoid opening the window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the webpage
url = "https://lubanastore.com/search?type=product&options%5Bprefix%5D=none&q=frock&options%5Bprefix%5D=last"
driver.get(url)

# Allow time for the page to load and execute JavaScript
time.sleep(5)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all the divs with background images (data-bgset)
image_divs = soup.find_all('div', class_='grid-view-item__image')

# Extract the image URLs from the data-bgset attribute
image_urls = []
for div in image_divs:
    data_bgset = div.get('data-bgset')
    if data_bgset:
        # Split the data-bgset to get individual image URLs
        images = [url.split(' ')[0] for url in data_bgset.split(',')]
        # Get the highest resolution image (last one in the list)
        highest_res_image = images[-1]
        image_urls.append("https:" + highest_res_image)

# Download the images
for idx, image_url in enumerate(image_urls):
    img_data = requests.get(image_url).content
    with open(f'image_{idx+1}.png', 'wb') as handler:
        handler.write(img_data)
    print(f'Downloaded: {image_url}')

# Close the driver
driver.quit()

