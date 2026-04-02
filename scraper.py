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
    """從檔案中提取舊新聞標題與網址，用來去重"""
    if not os.path.exists('result.txt'):
        return []
    
    with open('result.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正規表達式抓取標題與網址
    # 格式：【來源】標題 \n 🔗 網址
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
        # 如果失敗，會在 GitHub Actions 的日誌中印出錯誤訊息
        print(f"❌ Notion 傳送失敗！狀態碼: {res.status_code}, 原因: {res.text}")
    return res.status_code

def crawl_news(keyword, existing_links):
    new_found = []
    
    # 1. 中時新聞 (透過 Google RSS)
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

    # 2. 自由時報
    ltn_url = f"https://search.ltn.com.tw/list?keyword={keyword}"
    res_ltn = requests.get(ltn_url, headers={'User-Agent': 'Mozilla/5.0'})
    if res_ltn.status_code == 200:
        soup = BeautifulSoup(res_ltn.text, 'html.parser')
        for item in soup.select('ul.list > li'):
            a_tag = item.find('a', class_='tit')
            if a_tag:
                title = a_tag.text.strip()
                link = a_tag.get('href')
                # 放寬標準：相信自由時報的搜尋結果，只要沒抓過 (不重複) 就收錄！
                if link not in existing_links:
                    new_found.append({"source": "自由", "title": title, "link": link})
                    add_to_notion(title, link, "自由")
                    
    return new_found

# --- 主程式 ---
keyword = "軍事衝突"
old_news_list = get_existing_data()
existing_links = {n['link'] for n in old_news_list}

# 執行爬蟲抓取新新聞
new_news = crawl_news(keyword, existing_links)

# 合併新舊新聞，並重新寫入檔案 (達成消除重複的效果)
total_news = old_news_list + new_news

if new_news:
    # 重新整理檔案內容
    output = f"🕒 最後更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    output += f"🔎 監控關鍵字：{keyword}\n"
    output += "="*30 + "\n\n"
    
    # 只記錄最近的 50 筆，避免檔案無限長大
    for news in total_news[-500:]:
        output += f"【{news['source']}】{news['title']}\n🔗 {news['link']}\n\n"
    
    output += "▼"*30 + "\n\n"
    
    # 用 'w' (覆寫) 而不是 'a' (附加)，這樣才能「消除重複」並保持整潔
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"✅ 成功抓取 {len(new_news)} 筆新新聞！")
else:
    print("目前沒有新新聞，result.txt 保持不變。")
