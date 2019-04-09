from selenium import webdriver

import uuid
import urllib.request
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
    result = list()

    # get source list
    f = open("source_list.txt", "a+")
    source_list = f.readlines()

    for image in images_info:
        image_link = image[0]
        image_title = image[1].replace("\\u0027", "")
        image_source = image[2]
        image_ext = os.path.basename(image_link.split(".")[-1])

        if image_source not in source_list:
            f.write(f"\n{image_source}")
            urllib.request.urlretrieve(image_link, f"{name}/{uuid.uuid4().hex}.{image_ext}")

    f.close()
    driver.quit()


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
