import os
import time
import json
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Constants
BASE_URL = "https://www.istockphoto.com/search/2/image?mediatype=photography&phrase=switzerland&page="
CHROMEDRIVER_PATH = "chromedriver.exe"
SAVE_DIR = "data/images"
META_FILE = "data/image_metadata.json"
os.makedirs(SAVE_DIR, exist_ok=True)

# Chrome setup
options = Options()
# options.add_argument("--headless")  # Optional silent mode
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

metadata = []

for page_num in range(1, 4):  # Pages 1–3
    print(f"\nScraping page {page_num}")
    driver.get(BASE_URL + str(page_num))
    time.sleep(3)

    # Scroll to trigger lazy loading
    for _ in range(8):
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)

    time.sleep(4)  # Let all images load

    figures = driver.find_elements(By.CSS_SELECTOR, "figure img")
    print(f"Found {len(figures)} images on page {page_num}")

    for idx, img in enumerate(figures):
        try:
            img_url = img.get_attribute("src")
            caption = img.get_attribute("alt") or "No caption"
            if img_url and img_url.startswith("http"):
                filename = f"switzerland_p{page_num}_{idx+1}.jpg"
                filepath = os.path.join(SAVE_DIR, filename)

                response = requests.get(img_url)
                image = Image.open(BytesIO(response.content))
                image.save(filepath)

                metadata.append({
                    "page": page_num,
                    "image_number": idx + 1,
                    "caption": caption,
                    "url": img_url,
                    "filename": filename
                })
                print(f"Saved {filename} | {caption[:50]}")
            else:
                print(f"Skipping image {idx + 1} — no valid src")
        except Exception as e:
            print(f"Error on image {idx + 1}: {e}")

driver.quit()

# Save metadata
os.makedirs(os.path.dirname(META_FILE), exist_ok=True)
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print(f"\nDone. {len(metadata)} images and captions saved.")
print(f"🗂️ Metadata file: {META_FILE}")
