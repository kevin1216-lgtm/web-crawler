import os
import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")

notion_headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_all_links_from_file():
    if not os.path.exists('result.txt'):
        return set()
    with open('result.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正規表達式找出所有以 http 開頭的網址
        return set(re.findall(r'https?://[^\s\n]+', content))

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
    res = requests.post(url, headers=notion_headers, json=data)
    # 如果失敗，會在 GitHub Log 顯示錯誤原因
    if res.status_code != 200:
        print(f"❌ Notion Error: {res.status_code}, {res.text}")
    return res.status_code

def crawl_news(keyword, history_links):
    new_results = []
    
    # 1. 中時爬取
    ct_url = f"https://news.google.com/rss/search?q=site:chinatimes.com+{keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    ct_res = requests.get(ct_url, headers={'User-Agent': 'Mozilla/5.0'})
    if ct_res.status_code == 200:
        soup = BeautifulSoup(ct_res.text, 'xml') # RSS 建議用 xml 解析
        for item in soup.find_all('item'):
            title = item.title.text.split(" - ")[0]
            link = item.link.text
            if link not in history_links:
                new_results.append({"source": "中時", "title": title, "link": link})
                add_to_notion(title, link, "中時")

    # 2. 自由爬取
    ltn_url = f"https://search.ltn.com.tw/list?keyword={keyword}"
    ltn_res = requests.get(ltn_url, headers={'User-Agent': 'Mozilla/5.0'})
    if ltn_res.status_code == 200:
        soup = BeautifulSoup(ltn_res.text, 'html.parser')
        for item in soup.select('ul.list > li'):
            a_tag = item.find('a', class_='tit')
            if a_tag:
                title = a_tag.text.strip()
                link = a_tag.get('href')
                if keyword in title and link not in history_links:
                    new_results.append({"source": "自由", "title": title, "link": link})
                    add_to_notion(title, link, "自由")
                    
    return new_results

# 執行
keyword = "軍事衝突"
history_links = get_all_links_from_file()
new_news = crawl_news(keyword, history_links)

if new_news:
    output = f"🕒 自動更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    output += f"🔎 監控關鍵字：{keyword}\n"
    output += "="*30 + "\n\n"
    for news in new_news:
        output += f"【{news['source']}】{news['title']}\n🔗 {news['link']}\n\n"
    
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(output + "▼"*30 + "\n\n")
else:
    print("沒有發現新的重複新聞。")
