# Task 2
import urllib.request
from bs4 import BeautifulSoup
import csv

HEADERS = {"User-Agent": "Mozilla/5.0"}
#  模仿使用著，避免被網站阻擋

# Function: 從網址下載資料並轉成Python物件
def get_soup(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as res:
        return BeautifulSoup(res.read().decode("utf-8"), "html.parser")

# Function: 取文章列表
def get_posts(root):
    posts = []
    for div in root.select("div.r-ent"): # 找出所有文章區塊
        title_tag = div.select_one(".title a") # 找文章標題連結
        like_tag = div.select_one(".nrec span") # 找推文數
        title = title_tag.text.strip() if title_tag else "(已刪除)" # 取得<a>內文字, 如文章被刪除，標題為"(已刪除)"
        like = like_tag.text if like_tag else "0" # 如沒有推文數，預設"0"
        link = "https://www.ptt.cc" + title_tag["href"] if title_tag else None # full article URL
        posts.append((title, like, link)) 
    return posts


# Function: 文章發文時間
def get_post_time(link):
    if not link: # 連結是否存在
        return "(no time)"
    soup = get_soup(link) 
    for meta in soup.select(".article-metaline"):
        tag = meta.select_one(".article-meta-tag")
        value = meta.select_one(".article-meta-value")
        if tag and tag.text == "時間" and value:
            return value.text
    return "(no time)"

# Function: 找PTT「上一頁」連結
def get_next_page(root):
    next_btn = root.find("a", string="‹ 上頁") # 找「上一頁」按鈕
    return "https://www.ptt.cc" + next_btn["href"] if next_btn else None
    # if next_btn else None
    # 如找到上一頁按鈕，回傳完整網址
    # 如沒找到，回傳 None

# PTT Steam Board URL
url = "https://www.ptt.cc/bbs/Steam/index.html"
all_rows = []

# 爬3頁資料
for _ in range(3):  # 爬3頁
    soup = get_soup(url) # 取當前頁面
    for title, like, link in get_posts(soup): # 取所有文章
        all_rows.append([title, like, get_post_time(link)]) # 加入時間data
    url = get_next_page(soup) # 取下一頁
    if not url:  # 如沒下一頁結束
        break

# Save to CSV
with open("articles.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["標題", "推文數", "發文時間"])
    writer.writerows(all_rows)


