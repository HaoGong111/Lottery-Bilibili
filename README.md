# LotteryOfBilibili
B站转发动态抽奖~半自动
***所谓半自动，就是不用自己转赞评以及打开网页了
但是仍需要扫码登录，自己收集抽奖链接放到links.txt中***
### **特点**
+ 采用Python + Selenium模拟人为操作
+ 可以抽官抽，非官抽，固定转赞评，评论内容在五条评论内随机选取，不会重复，避免触发机器验证。
+ 为防止被检测，采用大量等待，每条耗时5-15s之间
### 使用方法
1. 安装Python3.x，并安装selenium库
```
pip install selenium
```
2. 下载与chrome版本匹配的ChromeDriver，并将其放到Python安装目录下的Scripts文件夹中
   1. 较新版本Chrome:[Chrome for Testing availability](https://googlechromelabs.github.io/chrome-for-testing/)
   2. [其他版本对应驱动](https://chromedriver.storage.googleapis.com/index.html)
3. 运行get_cookies.py，登录B站账号，此时会生成cookies.json文件
4. 将抽奖链接放入links.txt中，每行一个链接
5. 运行lottery.py，程序会自动开始抽奖
