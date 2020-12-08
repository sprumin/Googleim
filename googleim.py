from selenium import webdriver

import numpy as np
import cv2
import uuid
import os
import re
import requests
import sys
import time



class Googleim(object):
    def __init__(self, keyword, download_log=False, error_log=False):
        self.driver = webdriver.Chrome("chromedriver")
        self.keyword = keyword
        self.download_log = download_log
        self.error_log = error_log

    def crawl_image(self):
        self.driver.get(f"https://www.google.co.kr/search?q={self.keyword}&tbm=isch")
        self.driver.implicitly_wait(3)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        pause = 0.5

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)

            try:
                element = self.driver.find_elements_by_id("smb")[0]
                element.click()
            except:
                pass

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

        images_info = re.findall(r"\"ou\":\"(.*?)\".*?\"pt\":\"(.*?)\".*?\"ru\":\"(.*?)\"", driver.page_source)
        
        return images_info

    def save_image(self, images_str):
        errors = []
        downloads = []

        for image in images_str:
            image_link = image[0]
            image_source = image[2]
            image_ext = os.path.basename(image_link.split(".")[-1])

            if image_source not in source_list:
                get_img = np.asarray(bytearray(requests.get(image_link).content), dtype="uint8")
                image = cv2.imdecode(get_img, cv2.IMREAD_COLOR)
                try:
                    cv2.imwrite(f"{self.keyword}/{uuid.uuid4().hex}.{image_ext}", image)
                except:
                    errors.append(image_source)
                else:
                    downloads.append(image_source)
        
        if self.download_log:
            save_log("download", downloads)
        
        if self.error_log:
            save_log("error", errors)
    
    def save_log(self, log_type, logs):
        with open(f"logs/{log_type}.log", "w") as f:
            for log in logs:
                f.write(log + "\n")

