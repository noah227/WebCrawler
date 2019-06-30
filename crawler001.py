# __Author__: NOAH227
# __Date__: 2019/6/26


import re
import time
import requests
from bs4 import BeautifulSoup
from src import test    # parent folder is src, here folder is omitted

"""
    This program is for the specific keyword scanning from given site, 
    once keyword is caught, message about will be sent.
"""


def get_url(link):
    html = requests.get(link)
    print(html)
    content = html.text
    # print(content)
    soup = BeautifulSoup(content, "lxml")
    lists = soup.find_all(class_="j_thread_list clearfix")
    return lists


def log_file(log_content):
    with open("log.txt", "a+", encoding="utf-8") as f:
        f.write(log_content+"\n")


url = "https://tieba.baidu.com/f?kw=qq%E9%A3%9E%E8%BD%A6&ie=utf-8"
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
#                          "AppleWebKit/537.36 (KHTML, like Gecko) "
#                          "Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
# proxy = {}  # not needed now.
home = "https://tieba.baidu.com"


if __name__ == "__main__":

    flag = True
    while flag:
        lists = get_url(url)  # get tag "li" lists of the url
        # a = 0
        for li in lists:
            title = li.a.get_text()  # get the title of the context
            title = re.sub(r"[\s]", "", title)
            count = len(re.findall(r"[bug]", title))  # find if there's  a related one
            # print(type(li))  #  <class 'bs4.element.Tag'>
            if count:   # keyword exists, next to send message to the specific address, then log files.
                href = home + li.a.get("href")
                reply_time = li.div.find("span", attrs={"class": "threadlist_reply_date pull_right j_reply_data"})
                reply_time = re.sub(r"[\s]", "", reply_time.get_text())
                # print("time:", reply_time, href)
                test.send_email(title, href)
                # print(reply_time, "--------")
                log_file(title + href + "\t" + reply_time)
                time.sleep(300)  # wait for 300s
                count = 0   # reset checking variable
            # print(a, title)
            # a += 1
            time.sleep(0.3)
        time.sleep(5)
        # print("==========")



