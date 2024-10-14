import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Initialize a set to store already downloaded image URLs
downloaded_images = set()

# List of patterns to exclude from downloading
exclude_patterns = [
    '170x', '65x', 'width=300'
]

# Function to download an image
def download_image(img_url, folder_name):
    if any(pattern in img_url for pattern in exclude_patterns):
        print(f"Skipping image: {img_url}")
        return
    
    if img_url not in downloaded_images:
        try:
            img_data = requests.get(img_url).content
            file_name = os.path.join(folder_name, img_url.split("/")[-1].split("?")[0])
            with open(file_name, 'wb') as img_file:
                img_file.write(img_data)
            downloaded_images.add(img_url)
            print(f"Image downloaded successfully: {img_url}")
        except Exception as e:
            print(f"Failed to download {img_url}: {str(e)}")
    else:
        print(f"Image already downloaded: {img_url}")

# Function to scrape images from a given URL
def scrape_images(url, folder_name="images"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Setup Selenium Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Find all image tags on the page
    images = driver.find_elements(By.TAG_NAME, 'img')

    # Extract the 'src' attribute for each image and download it
    for img in images:
        img_url = img.get_attribute('src')
        if img_url:
            download_image(img_url, folder_name)

    driver.quit()

# List of URLs to scrape
urls = [

   
    
    
    'https://silkandsaffron.store/products/botanical-bliss-long-dress?_pos=4&_sid=3ffb91762&_ss=r',
    'https://silkandsaffron.store/products/victoria-long-dress-by-silk-and-saffron?_pos=7&_sid=3ffb91762&_ss=r',
    
    'https://silkandsaffron.store/products/liliosa-green-floral-long-dress-by-silk-and-saffron?_pos=14&_sid=3ffb91762&_ss=r',
    
    
    
    
    
    
    'https://silkandsaffron.store/products/dahlia-long-dress-by-silk-and-saffron?_pos=8&_sid=3ffb91762&_ss=r'
]

# Iterate through each URL and scrape images
for url in urls:
    scrape_images(url)

'''
'https://silkandsaffron.store/products/black-swan-long-dress-by-silk-and-saffron?_pos=16&_sid=3ffb91762&_ss=r',
'https://silkandsaffron.store/products/nova-black-dress?_pos=5&_sid=3ffb91762&_ss=r',
    'https://silkandsaffron.store/products/isla-long-dress?_pos=1&_sid=3ffb91762&_ss=r',
    'https://silkandsaffron.store/products/pastel-petals-long-dress?_pos=6&_sid=3ffb91762&_ss=r',
     'https://silkandsaffron.store/products/blossom-serenade-long-dress?_pos=2&_sid=3ffb91762&_ss=r',
     'https://silkandsaffron.store/products/pink-mirage-long-dress?_pos=3&_sid=3ffb91762&_ss=r',
    'https://silkandsaffron.store/products/audra-floral-long-dress?_pos=10&_sid=3ffb91762&_ss=r',
    'https://silkandsaffron.store/products/azure-smock-long-dress-from-silk-and-saffron?_pos=12&_sid=3ffb91762&_ss=r',
'https://silkandsaffron.store/products/calla-floral-long-dress-by-silk-and-saffron?_pos=11&_sid=3ffb91762&_ss=r',
'https://silkandsaffron.store/products/blush-mosaic-long-dress?_pos=15&_sid=3ffb91762&_ss=r'
    'https://silkandsaffron.store/products/carlin-audra-long-dress-by-silk-and-saffron?_pos=13&_sid=3ffb91762&_ss=r',
    'https://silkandsaffron.store/products/farrah-long-dress?_pos=9&_sid=3ffb91762&_ss=r',

    
    '''