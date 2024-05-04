import json
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
# options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
options.add_experimental_option(
    "excludeSwitches", ["enable-automation", "enable-logging"]
)
browser = webdriver.Chrome(options=options)
comments = ["来了来了[脱单doge]", "就想简简单单中个奖QAQ", "啊啊啊啊啊, 让我中一次吧 T_T", "天选之子[doge]"]
link_list=[]
num=0

def gethtml():
    """
    免登录访问B站
    """
    url = input("输入抽奖合集网址：")
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


def crawl_links():
    """
    获取页面所有抽奖链接
    """
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    print(
        " ------------------------------------------- 分割线 -------------------------------------------------\n\n"
    )
    alinks = soup.find_all(["a"], {"class": "article-link"})
    i = 0
    del alinks[0]
    with open("../links.txt", "w", encoding="utf-8") as f:
        for alink in alinks:
            # 文章中所有链接
            link = alink.get_text()  # 23到40位为id，取ii[23:41]
            # 写入文件
            print(link, file=f)
            i += 1
    print("共输入{}个链接".format(i))


def dynamic(url):
    browser.get(url)
    time.sleep(1+random.random())
    # 关注s
    profile = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div')
    ActionChains(browser).move_to_element(profile).perform()
    time.sleep(1)
    follow = browser.find_element_by_css_selector(
        ".bili-user-profile-view__info__button.follow"
    )
    if "checked" not in follow.get_attribute("class"):
        follow.click()
    
    # 鼠标移向别处
    other_place = browser.find_element_by_xpath('//*[@id="nav-searchform"]/div[1]/input')
    ActionChains(browser).move_to_element(other_place).perform()
    time.sleep(1)

    # 点赞
    try:
        like = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[4]/div[3]/div')
    except:
        browser.execute_script("window.scrollTo(0, document.body.scrollTop=100);")
        time.sleep(1)
        like = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[4]/div[3]/div')
            )
        )
    like.click()

    for i in range(10): # 慢慢向下滑动窗口，让所有商品信息加载完成
        browser.execute_script('window.scrollTo(0, {});'.format(i*100))
        time.sleep(0.1)
    time.sleep(1)
    target = browser.find_element_by_class_name("tabs-order")
    browser.execute_script("arguments[0].scrollIntoView();", target) # 拖动到可见的元素去

    # 输入评论
    comment_box = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/textarea')
    """except:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        comment_box = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/textarea')
            )
        )"""
    comment_box.clear()
    comment_box.send_keys(random.choice(comments))

    # 勾选 同时转发到我动态
    also_forward = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[3]/div[4]/label')
    """except:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        also_forward = browser.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[3]/div[4]/label'
        )"""
    also_forward.click()

    # 发表评论
    publish_comment = browser.find_element_by_xpath(
        '//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/button'
    )
    publish_comment.click()
    global num
    num = num + 1
    print(str(num)+"：已成功转发动态{}".format(url[23:41]))
    time.sleep(1 + random.random())


def get_url():
    # 读取今天的链接
    txt_file = open('../links.txt', 'r', encoding='utf-8')
    for content in txt_file.readlines():
        link_list.append(content.strip('\n'))
    txt_file.close()


if __name__ == "__main__":
    gethtml()
    crawl_links()
    get_url()

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
