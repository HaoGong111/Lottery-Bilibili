
import random
comment_box = ["来了来了[脱单doge]", 
            "就想简简单单中个奖QAQ",
            "啊啊啊啊啊, 让我中一次吧 T_T",
            "天选之子[doge]",
            "好耶，感谢[星星眼][星星眼][星星眼]"]
link_list=[]
num=0


def random_comment():
    global comments
    li = comments[:-1]
    pick = random.choice(li)
    idx = comments.index(pick)
    comments[idx], comments[4] = comments[4], comments[idx]
    return pick

for i in range(10):
    print(random_comment())