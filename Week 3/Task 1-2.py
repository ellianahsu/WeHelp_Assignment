# Task 2/2

import urllib.request
import json
import csv

url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"

# 下載 轉JSON
with urllib.request.urlopen(url) as res:
    hotels = json.load(res)["list"]

districts = {}

for h in hotels:
    # try-except 預防沒有「市」導致程式崩潰: 
    try:
        district = h["地址"].split("市")[1].split("區")[0] + "區"
    except IndexError:
        district = "其他" # 如出錯，設為「其他」
    rooms = int(h["房間數"])

    d = districts.setdefault(district, {"飯店數": 0, "房間數": 0})
    # setdefault：
    # 1. 在 districts 加入 "中山區": {"飯店數": 0, "房間數": 0}
    # 2. 回傳這個字典給 d

    d["飯店數"] += 1
    d["房間數"] += rooms

"""
"台北市中山區南京東路"
        ↓ split("市")
    ["台北", "中山區南京東路"]
              ↓ [1] 取索引1
         "中山區南京東路"
              ↓ split("區")
         ["中山", "南京東路"]
            ↓ [0] 取索引0
            "中山"
              ↓ + "區"
            "中山區"
"""


# 寫入CSV
with open("districts.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["行政區", "飯店數", "房間數"])
    writer.writerows([[k, v["飯店數"], v["房間數"]] for k, v in districts.items()])
