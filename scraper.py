import os
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

# --- 環境變數讀取 ---
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")

notion_headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 讀取舊紀錄：確保不會重複抓取
def get_existing_history():
    if not os.path.exists('result.txt'):
        return ""
    with open('result.txt', 'r', encoding='utf-8') as f:
        return f.read()

# 新增至 Notion：保留狀態碼回傳，方便日後擴充報錯功能
def add_to_notion(title, link, source):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Name": { "title": [{"text": {"content": title}}] },
            "URL": { "url": link },
            "Source": { "select": {"name": source} },
            "Date": { "date": {"start": datetime.now().isoformat()} }
        }
    }
    response = requests.post(url, headers=notion_headers, json=data)
    return response.status_code

def crawl_china_times(keyword, history):
    # 使用 Google News RSS 比較穩定
    url = f"https://news.google.com/rss/search?q=site:chinatimes.com+{keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    # 完整的 User-Agent 降低被封鎖機率
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=req_headers)
    results = []
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.find_all('item')
        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            if title_tag and link_tag:
                link = link_tag.text
                # 檢查重複：如果網址已存在則跳過
                if link in history:
                    continue
                # 乾淨標題處理
                clean_title = title_tag.text.split(" - ")[0]
                results.append(f"【中時】{clean_title}\n🔗 {link}")
                add_to_notion(clean_title, link, "中時")
    return results 

def crawl_ltn(keyword, history):
    url = f"https://search.ltn.com.tw/list?keyword={keyword}"
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=req_headers)
    results = []
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.select('ul.list > li')
        for item in items:
            a_tag = item.find('a', class_='tit')
            if a_tag:
                title = a_tag.text.strip()
                link = a_tag.get('href')
                # 檢查關鍵字與重複性
                if keyword in title and link not in history:
                    results.append(f"【自由】{title}\n🔗 {link}")
                    add_to_notion(title, link, "自由")
    return results

# --- 主要執行區塊 ---
keyword = "軍事衝突"
history_content = get_existing_history()

all_news = []
all_news.extend(crawl_china_times(keyword, history_content))
all_news.extend(crawl_ltn(keyword, history_content))

# 視覺化排版寫入檔案
if all_news:
    output = f"🕒 自動更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    output += f"🔎 監控關鍵字：{keyword}\n"
    output += "="*30 + "\n\n"
    output += "\n\n".join(all_news)
    
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(output)
        # 加入美觀的分隔線
        f.write("\n\n" + "▼"*30 + "\n\n")
else:
    print(f"{datetime.now().strftime('%H:%M:%S')} - 目前無新新聞。")
