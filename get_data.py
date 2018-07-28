import sys
import os
from selenium import webdriver
import pandas
import time
import re
import csv

browser = webdriver.Chrome(executable_path='C:/driver/chromedriver.exe')

#1
#コマンドライン引数で値が取ってくるように
args = sys.argv
df = pandas.read_csv('default.csv', index_col=0)

#2
#コマンドライン引数を
#引数が入っていればすべてargs[1]に入る(空白があっても)
query = args[1]


#3
#キーワード検索
browser.get("https://www.mercari.com/jp/search/?sort_order=price_desc&keyword={}&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=".format(query))

#4
page = 1
while True: #continue until getting the last page

    #5-1
    #次のページが存在する場合データを取得
    print("******************page: {} ***********************".format(page))
    print("Starting to get posts...")

    #5-1-2
    #アイテムを取得
    posts = browser.find_elements_by_css_selector(".items-box")

    #5-1-3
    for post in posts:
        #アイテムボックスの中の名前を取得
        title = str(post.find_element_by_css_selector("h3.items-box-name").text)
        title = re.sub('【|】|《|》|❤︎|♡|①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|★|➕|❗|☆|⭐︎|～|・|『|』|◎|◆|■|□|◇|☺︎|‼️|✖︎|☆彡|☆ミ|✨|⚠|⊿|❗️|⭐︎|〜|️️⭐️','',title)
        title = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", title)
        title = re.sub(r'[!-~]', "", title)#半角記号,数字,英字
        title = re.sub(r'[︰-＠]', "", title)#全角記号

        #5-1-3-1
        #値段を取得
        price = post.find_element_by_css_selector(".items-box-price").text
        price = price.replace('¥', '')
        #いいねがあるときは数え、ないときは０
        try:
            like = post.find_element_by_css_selector("div.items-box-likes.font-2 > span").text
        except:
            like = 0
        #5-1-3-2
        #ソールド帯がついていたらsold=1にする
        sold = 0
        if len(post.find_elements_by_css_selector(".item-sold-out-badge")) > 0:
            sold = 1

        url = post.find_element_by_css_selector("a").get_attribute("href")

        #データフレームに格納
        list = [title,like,price,url,sold]

        #CSVに書き込み
        print(list)
        try:
            with open('***.csv','a',newline="",encoding="sjis") as f:
                writer = csv.writer(f)
                writer.writerow(list)
                print('ok')
        except:
            continue


    #次のページがあるかどうか
    page+=1
    if len(browser.find_elements_by_css_selector("body > div > main > div.l-content > ul > li.pager-next.visible-pc > ul > li:nth-child(1)")) == 0:
        #なければ終了
        print("no pager exist anymore")
        break

    #ある場合、次ページのURLを取得
    btn = browser.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
    browser.get(btn)
    print("Moving to next page......")

browser.quit()
