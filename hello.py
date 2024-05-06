import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from utils import read_urls, url2id

options = Options()
#options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
options.add_experimental_option(
    "excludeSwitches", ["enable-automation", "enable-logging"]
)
browser = webdriver.Chrome(options=options)
browser.get("https://t.bilibili.com/920923026455789587")
# browser.get("https://t.bilibili.com/926028033187381272")
try:
    browser.find_element(By.CLASS_NAME, "reference")
    print(True)
except Exception as e:
    print(e)
    print(False)
browser.close()