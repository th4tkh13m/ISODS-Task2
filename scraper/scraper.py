import requests
from PIL import Image
from io import BytesIO
from .config import AI_URL, TRUE_URL, NUM_IMAGES, WAIT_TIME
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class Scraper():
    def __init__(self) -> None:
        self.driver = self.get_driver()
        self.true_imgs = []
        self.ai_imgs = []

    def get_driver(self):
        options = Options()
        options.headless = True
        return webdriver.Firefox(
            options
        )

    def fetch_ai_images(self, query, num_images=NUM_IMAGES):
        self.driver.get(AI_URL.format(q=query))
        self.ai_imgs = []
        i = 0
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            wait = WebDriverWait(self.driver, WAIT_TIME)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="gridcell"]')))
            time.sleep(WAIT_TIME)
            elements = self.driver.find_elements(By.XPATH, '//div[@role="gridcell"]')
            for element in elements:
                img_url = element.find_element(By.TAG_NAME, "img").get_attribute("src")
                if not img_url in self.ai_imgs:
                    self.ai_imgs.append(img_url)
                    i += 1
                    if i >= num_images:
                        return
                    
    def fetch_true_images(self, query, num_images=NUM_IMAGES):
        self.driver.get(TRUE_URL.format(q=query))
        self.true_imgs = []
        i = 0
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            wait = WebDriverWait(self.driver, WAIT_TIME)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'article')))
            time.sleep(WAIT_TIME)
            articles = self.driver.find_elements(By.TAG_NAME, 'article')
            for article in articles:
                img_url = article.find_element(By.TAG_NAME, "img").get_attribute("src")
                if not img_url in self.true_imgs:
                    self.true_imgs.append(img_url)
                    i += 1
                    if i >= num_images:
                        return

    def _get_image(url, img_path):
        try:
            with requests.get(url) as resp:
                with Image.open(BytesIO(resp.content)) as img:
                    new_img = img.resize((300, 300))
                    new_img.save(img_path)
            return True
        except:
            return False
        
    def _save_images(img_list, save_dir):
        for i, img_url in enumerate(img_list):
            img_path = os.path.join(save_dir, f"{i}.png")
            Scraper._get_image(img_url, img_path)
    
    def save_ai_images(self, save_dir):
        ai_dir = os.path.join(save_dir, "ai")
        os.makedirs(ai_dir, exist_ok=True)
        Scraper._save_images(self.ai_imgs, ai_dir)

    def save_true_images(self, save_dir):
        true_dir = os.path.join(save_dir, "true")
        os.makedirs(true_dir, exist_ok=True)
        Scraper._save_images(self.true_imgs, true_dir)
            
    def quit_driver(self):
        self.driver.quit()