import re
import random
from typing import List

CONST_URL_PREFIX = "https://t.bilibili.com/"
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
