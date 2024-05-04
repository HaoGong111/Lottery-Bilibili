import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from utils import random_comment, read_urls, url2id

options = Options()
#options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
options.add_experimental_option(
    "excludeSwitches", ["enable-automation", "enable-logging"]
)
browser = webdriver.Chrome(options=options)

link_list=[]
num=0


def gethtml():
    """
    免登录访问B站
    """
    url = "https://www.bilibili.com"
    browser.get(url)
    browser.maximize_window()
    # 删除这次登录时，浏览器自动储存到本地的cookie
    browser.delete_all_cookies()

    # 读取之前已经储存到本地的cookie
    cookies_filename = "./cookies.json"
    cookies_file = open(cookies_filename, "r", encoding="utf-8")
    cookies_list = json.loads(cookies_file.read())
    for cookie in cookies_list:  # 把cookie添加到本次连接
        browser.add_cookie(
            {
                "domain": ".bilibili.com",  # 此处xxx.com前，需要带点
                "name": cookie["name"],
                "value": cookie["value"],
                "path": "/",
                "expires": None,
            }
        )
    # 再次访问网站，由于cookie的作用，从而实现免登陆访问
    browser.get(url)
    time.sleep(3)

def check_origin_exists():
    """
    是否存在动态引用
    """
    try:
        browser.find_element(By.CLASS_NAME, "bili-dyn-content__orig reference")
        return True
    except:
        return False

def official():
    try:
        official_icon = browser.find_element(By.CSS_SELECTOR, ".bili-rich-text-module.lottery")
        official_icon.click()
        iframe = browser.find_element(By.CLASS_NAME, 'bili-popup__content__browser')
        browser.switch_to.frame(iframe)
        button = browser.find_element(By.CLASS_NAME, "join-button")
        time.sleep(2)
        button.click()
        browser.switch_to.default_content()
        num = num + 1
        print(str(num)+"：已成功转发official动态{}".format(url2id(url)))
        return True
    except:
        return False
    finally:
        time.sleep(7 * random.random())


def dynamic(url):
    browser.get(url)
    time.sleep(1+random.random())
    if official():
        return
    # 关注s
    profile = browser.find_element(By.CLASS_NAME, "bili-dyn-avatar")
    ActionChains(browser).move_to_element(profile).perform()
    time.sleep(1)
    follow = browser.find_element(By.CSS_SELECTOR, ".bili-user-profile-view__info__button.follow")
    if "checked" not in follow.get_attribute("class"):
        follow.click()
    
    # 鼠标移向别处
    other_place = browser.find_element(By.XPATH, '//*[@id="nav-searchform"]/div[1]/input')
    ActionChains(browser).move_to_element(other_place).perform()
    time.sleep(3+random.random())

    for i in range(10): # 慢慢向下滑动窗口，让所有信息加载完成
        browser.execute_script('window.scrollTo(0, {});'.format(i*100))
        time.sleep(0.1)
    time.sleep(1)
    target = browser.find_element(By.CLASS_NAME, "bili-tabs__nav__items")
    browser.execute_script("arguments[0].scrollIntoView();", target) # 拖动到可见的元素去
    time.sleep(3 * random.random())
    
    # 输入评论
    comment_box = browser.find_element(By.TAG_NAME, "textarea")
    comment_box.clear()
    time.sleep(1)
    comment_box.send_keys(random_comment())
    # 勾选 同时转发到我动态
    browser.find_element(By.ID, "forwardToDynamic").click()
    
    time.sleep(1)
    # 发表评论
    publish_comment = browser.find_element(By.CLASS_NAME, "send-text").click()
    num = num + 1
    print(str(num)+"：已成功转发动态{}".format(url2id(url)))
    time.sleep(7 * random.random())


if __name__ == "__main__":
    link_list = read_urls()
    gethtml()
    
    note = open('./link_history.txt', 'a+', encoding="utf-8")
    note.seek(0)
    history= note.read().split('\n')
    for url in link_list:
        id=url[23:41]
        if id not in history:
            try:
                dynamic(url)
            except:
                continue
            note.write(id+'\n')
    note.close()
    
    browser.close()
