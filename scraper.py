import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

NOTION_TOKEN = "您的_Internal_Integration_Secret"
DATABASE_ID = "您的_Database_ID"

notion_headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

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
    requests.post(url, headers=notion_headers, json=data)

def crawl_china_times(keyword):
    url = f"https://news.google.com/rss/search?q=site:chinatimes.com+{keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    res = requests.get(url, headers=req_headers)
    results = []
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.find_all('item')
        
        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            
            if title_tag and link_tag:
                title = title_tag.text
                link = link_tag.text
                clean_title = title.split(" - ")[0]
                
                results.append(f"【中時】{clean_title}\n🔗 {link}")
                add_to_notion(clean_title, link, "中時")
                
        if len(results) == 0:
            results.append(f"⚠️ 【中時】連線成功，但 Google 尚未收錄「{keyword}」的最新新聞。")
    else:
        results.append(f"❌ 【中時】連線失敗 (狀態碼: {res.status_code})")
        
    return results 

def crawl_ltn(keyword):
    url = f"https://search.ltn.com.tw/list?keyword={keyword}"
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
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
                
                if keyword in title:
                    results.append(f"【自由】{title}\n🔗 {link}")
                    add_to_notion(title, link, "自由")
                    
        if len(results) == 0:
            results.append(f"⚠️ 【自由】網頁連線成功，但目前沒有「{keyword}」的最新新聞。")
    else:
        results.append(f"❌ 【自由】連線失敗，可能被網站阻擋了 (狀態碼: {res.status_code})")
        
    return results

keyword = "軍事衝突"
all_news = []
all_news.extend(crawl_china_times(keyword))
all_news.extend(crawl_ltn(keyword))

output = f"🕒 自動更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
output += f"🔎 監控關鍵字：{keyword}\n"
output += "="*30 + "\n\n"
output += "\n\n".join(all_news)

with open('result.txt', 'a', encoding='utf-8') as f:
    f.write(output)
    f.write("\n" + "▼"*30 + "\n\n")
