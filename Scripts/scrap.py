import requests
from bs4 import BeautifulSoup
import os
import sys
import random
import time
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
]

def get_random_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }

def download_images(url, folder):
    if not os.path.exists(folder):
        logging.error(f"Folder does not exist: {folder}")
        return  # Exit if folder does not exist
    
    logging.info(f"Using existing folder: {folder}")
    
    session = requests.Session()
    session.headers.update(get_random_header())
    response = session.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to fetch the page, status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    logging.info(f"Found {len(images)} images.")
    
    for image in images:
        src = image.get('src') or image.get('data-src')
        if not src or not src.startswith(('http', '//')):
            logging.warning(f"Skipping non-http source or missing source: {src}")
            continue
        if src.startswith('//'):
            src = 'https:' + src
        
        img_response = session.get(src)
        if img_response.status_code == 200:
            img_data = img_response.content
            img_hash = hashlib.md5(img_data).hexdigest()
            filename = f'{img_hash}.jpg'
            file_path = os.path.join(folder, filename)
            if os.path.exists(file_path):
                logging.info(f"File already exists, skipping: {file_path}")
                continue
            
            with open(file_path, 'wb') as file:
                file.write(img_data)
                logging.info(f'Downloaded: {filename}')
        else:
            logging.error(f"Failed to download {src}, status code: {img_response.status_code}")
        
        time.sleep(random.uniform(0.5, 2))  # Respect server load

if __name__ == '__main__':
    if len(sys.argv) > 2:
        url = sys.argv[1]
        folder = sys.argv[2]
        download_images(url, folder)
    else:
        print("Usage: python script.py <url> <folder>")



