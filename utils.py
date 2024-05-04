import re
import random
from typing import List

CONST_URL_PREFIX = "https://t.bilibili.com/"
comment_box = ["来了来了[脱单doge]", 
            "就想简简单单中个奖QAQ",
            "啊啊啊啊啊, 让我中一次吧 T_T",
            "天选之子[doge]",
            "好耶，感谢[星星眼][星星眼][星星眼]"]
LINKS_PATH = "./links.txt"


def url2id(s):
    matches = re.findall(r'\d+', s)
    if matches:
        return matches[0]
    else:
        return None

def new_dynamic_url_to_old(url):
    id = url2id(url)
    if id is None:
        return id
    return CONST_URL_PREFIX + str(id)

def read_urls() -> List[str]:
    txt_file = open(LINKS_PATH, 'r', encoding='utf-8')
    link_list = []
    for content in txt_file.readlines():
        if content.startswith("https://www.bilibili.com/opus"):
            url = new_dynamic_url_to_old(content.strip('\n'))
            if url is not None:
                link_list.append(url)
        else:
            link_list.append(content.strip('\n'))
    txt_file.close()
    return link_list

# 初始化一个用于跟踪评论状态的列表
def random_comment():
    global comments
    li = comments[:-1]
    pick = random.choice(li)
    idx = comments.index(pick)
    comments[idx], comments[4] = comments[4], comments[idx]
    return pick
