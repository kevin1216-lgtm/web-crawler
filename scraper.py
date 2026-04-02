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

def get_existing_data():
    if not os.path.exists('result.txt'):
        return []
    
    with open('result.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r"【(?P<source>.*?)】(?P<title>.*?)\n🔗 (?P<link>https?://[^\s\n]+)"
    matches = re.finditer(pattern, content)
    
    existing_news = []
    for m in matches:
        existing_news.append({
            "source": m.group("source"),
            "title": m.group("title").strip(),
            "link": m.group("link").strip()
        })
    return existing_news

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
    if res.status_code != 200:
        print(f"❌ Notion 傳送失敗！狀態碼: {res.status_code}, 原因: {res.text}")
    return res.status_code

def crawl_news(keyword, existing_links):
    new_found = []
    
    ct_url = f"https://news.google.com/rss/search?q=site:chinatimes.com+{keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    res_ct = requests.get(ct_url, headers={'User-Agent': 'Mozilla/5.0'})
    if res_ct.status_code == 200:
        soup = BeautifulSoup(res_ct.text, 'xml')
        for item in soup.find_all('item'):
            title = item.title.text.split(" - ")[0]
            link = item.link.text
            if link not in existing_links:
                new_found.append({"source": "中時", "title": title, "link": link})
                add_to_notion(title, link, "中時")

    ltn_url = f"https://search.ltn.com.tw/list?keyword={keyword}&sort=date"
    res_ltn = requests.get(ltn_url, headers={'User-Agent': 'Mozilla/5.0'})
    if res_ltn.status_code == 200:
        soup = BeautifulSoup(res_ltn.text, 'html.parser')
        for item in soup.select('ul.list > li'):
            a_tag = item.find('a', class_='tit')
            if a_tag:
                title = a_tag.text.strip()
                link = a_tag.get('href')
                if link not in existing_links:
                    new_found.append({"source": "自由", "title": title, "link": link})
                    add_to_notion(title, link, "自由")
                    
    return new_found

keyword = "軍事衝突"
old_news_list = get_existing_data()
existing_links = {n['link'] for n in old_news_list}

new_news = crawl_news(keyword, existing_links)

total_news = new_news + old_news_list

if new_news:
    output = f"🕒 最後更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    output += f"🔎 監控關鍵字：{keyword}\n"
    output += "="*30 + "\n\n"
    
    for news in total_news[:500]:
        output += f"【{news['source']}】{news['title']}\n🔗 {news['link']}\n\n"
    
    output += "▼"*30 + "\n\n"
    
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"✅ 成功抓取 {len(new_news)} 筆新新聞！")
else:
    print("目前沒有新新聞，result.txt 保持不變。")
