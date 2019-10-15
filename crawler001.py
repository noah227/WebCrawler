# __Author__: NOLA
# __Date__: 2019/6/26


import re
import time
import random
import requests
from bs4 import BeautifulSoup
from src import mailman

"""
    This program is for the specific keyword scanning from given site, 
    once keyword is caught, message about will be sent to specific receiver.
"""


def get_url(link):
    # this project requests almost no security, thus we don't use verify here
    html = requests.get(link, verify=False)
    print(html)
    content = html.text
    # print(content)
    soup = BeautifulSoup(content, "lxml")
    lists = soup.find_all(class_="j_thread_list clearfix")
    return lists


def log_file(log_content):
    with open("log.txt", "a+", encoding="utf-8") as f:
        f.write(log_content + "\n")


url = "https://tieba.baidu.com/f?kw=qq%E9%A3%9E%E8%BD%A6&ie=utf-8"
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
#                          "AppleWebKit/537.36 (KHTML, like Gecko) "
#                          "Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
# proxy = {}  # not needed now.
home = "https://tieba.baidu.com"


def crawler(query_message):
    flag = True
    while flag:
        # get tag "li" lists of the url
        lists = get_url(url)
        a = 0
        for li in lists:
            # get the title of the context
            title = li.a.get_text()
            title = re.sub(r"[\s]", "", title)
            # find if there's  a related one
            count = len(re.findall(r"[%s]" % query_message, title))
            href = home + li.a.get("href")
            # print(type(li))  #  <class 'bs4.element.Tag'>
            print(href)
            # keyword exists, next to send message to the specific address, then log files.
            if count:
                href = home + li.a.get("href")
                reply_time = li.div.find("span", attrs={"class": "threadlist_reply_date pull_right j_reply_data"})
                reply_time = re.sub(r"[\s]", "", reply_time.get_text())
                print("time:", reply_time, href)
                mailman.send_email(title, href)
                print(reply_time, "--------")
                log_file(title + href + "\t" + reply_time)
                # wait for 300s
                time.sleep(300)
                # reset checking variable
                count = 0
            print(a, title)
            a += 1
            time.sleep(0.3)
        # a random time wait for simple anti-block
        time.sleep(random.randint(1, 6))
        print("==========")


if __name__ == "__main__":
    crawler("A")
    pass





