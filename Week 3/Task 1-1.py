# Task 1/2

import urllib.request  # 下載網路資料
import json             # JSON轉成Python
import csv              # 資料寫入CSV 

# Dict for CH/EN URL
urls = {
    "ch": "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch",
    "en": "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en",
}

# Function：從網址下載資料並轉成Python物件. Pro: 不須寫兩次
def load_json(url):
    # urllib 開啟網址
    with urllib.request.urlopen(url) as res:
        # 讀取JSON轉成Python資料，取出"list"裡的資料
        return json.load(res)["list"]

# Download CH/EN dataset
ch_list = load_json(urls["ch"])
en_list = load_json(urls["en"])

# 建立快速查找英文資料的Dict（"_id" 當鍵key）
en_dict = {item["_id"]: item for item in en_list}
# {鍵: 值 for 變數 in 列表}

# 開啟新的 CSV，寫入整理後飯店資料
with open("hotels.csv", "w", newline="", encoding="utf-8-sig") as f:
    # newline="" 避免生多餘空行
    # encoding="utf-8-sig" 避免中文亂碼
    writer = csv.writer(f)  
    # 寫入欄位標題 col header
    writer.writerow(["chinese_name", "english_name", "chinese_address", "english_address", "phone", "room_count"])
    
    # For Loop: 比對中文與英文資料，寫入CSV
    for ch in ch_list:
        en = en_dict.get(ch["_id"])  # "_id"對應英文資料
        if en:  # 如果有找到英文資料
            writer.writerow([
                ch["旅宿名稱"],       
                en["hotel name"],    
                ch["地址"],           
                en["address"],         
                en.get("tel", ""),     # 若無電話，用get預設值避免程式崩潰
                ch["房間數"],          
            ])

