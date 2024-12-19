from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests

def search_paintings_selenium(query, count=10):
    """
    Use Selenium to scrape images from DuckDuckGo for a given query.
    """
    search_url = f"https://duckduckgo.com/?q={query}+paintings&iar=images&iax=images&ia=images"
    driver = webdriver.Chrome()  # Replace with your WebDriver (e.g., Firefox, Edge)
    driver.get(search_url)
    time.sleep(5)  # Wait for JavaScript to load content

    # Find image elements
    images = driver.find_elements(By.TAG_NAME, "img")
    image_urls = []
    for img in images:
        src = img.get_attribute("src")
        if src and src.startswith("http"):  # Filter for valid image URLs
            image_urls.append(src)
        if len(image_urls) >= count:
            break

    driver.quit()
    return image_urls

def download_images(image_urls, folder="paintings"):
    """
    Download images from a list of URLs.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(os.path.join(folder, f"painting_{idx + 1}.jpg"), "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
            print(f"Downloaded: {url}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    search_term = input("Enter a word/phrase to search for paintings: ")
    print(f"Searching for paintings related to '{search_term}'...")
    image_urls = search_paintings_selenium(search_term, count=10)

    if image_urls:
        print("Found images, downloading them...")
        download_images(image_urls)
        print("Download completed. Check the 'paintings' folder.")
    else:
        print("No images found.")
