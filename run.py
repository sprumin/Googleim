from selenium import webdriver

import numpy as np
import cv2
import uuid
import os
import re
import requests
import sys
import time


def crawl_google_image(name):
    driver = webdriver.Chrome("chromedriver")
    driver.get(f"https://www.google.co.kr/search?q={name}&tbm=isch")
    driver.implicitly_wait(3)

    last_height = driver.execute_script("return document.body.scrollHeight")
    pause = 0.5

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

        try:
            element = driver.find_elements_by_id("smb")[0]
            element.click()
        except:
            pass

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    # [0]: image_link, [1]: title, [2]: source
    images_info = re.findall(r"\"ou\":\"(.*?)\".*?\"pt\":\"(.*?)\".*?\"ru\":\"(.*?)\"", driver.page_source)
    driver.quit()

    # get source list
    f = open("source_list.txt", "r+")
    source_list = f.read().split("\n")
    os.chdir(name)

    for image in images_info:
        image_link = image[0]
        # image_title = image[1].replace("\\u0027", "") 현재 사용하지 않음.
        image_source = image[2]
        image_ext = os.path.basename(image_link.split(".")[-1])

        if image_source not in source_list:
            get_img = np.asarray(bytearray(requests.get(image_link).content), dtype="uint8")
            image = cv2.imdecode(get_img, cv2.IMREAD_COLOR)
            try:
                cv2.imwrite(f"{uuid.uuid4().hex}.{image_ext}", image)
            except:
                print(f"SAVE ERROR : {image_source}")
            else:
                f.write(f"\n{image_source}")
                print(f"SAVE DATA : {image_source}")
        else:
            print(f"Image already exists")

    f.close()


def main():
    name = sys.argv[1]

    try:
        f = open("source_list.txt", "r")
    except:
        with open("source_list.txt", "w") as f:
            f.write("# SOURCE LIST")

    if not(os.path.isdir(name)):
        os.makedirs(os.path.join(name))

    crawl_google_image(name)


if __name__ == "__main__":
    main()
