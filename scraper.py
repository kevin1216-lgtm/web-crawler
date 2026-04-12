import os
import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
                    
    bbc_url = f"https://news.google.com/rss/search?q=site:bbc.com/zhongwen+{keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    res_bbc = requests.get(bbc_url, headers={'User-Agent': 'Mozilla/5.0'})
    if res_bbc.status_code == 200:
        soup = BeautifulSoup(res_bbc.text, 'xml')
        for item in soup.find_all('item'):
            title = item.title.text.split(" - ")[0]
            link = item.link.text
            if link not in existing_links:
                new_found.append({"source": "BBC", "title": title, "link": link})
                add_to_notion(title, link, "BBC")
                    
    return new_found

# 🌟 新增的函式：製作文字雲
def generate_wordcloud(news_list):
    if not news_list:
        return
    
    # 將所有標題接在一起
    all_titles = " ".join([news['title'] for news in news_list])
    
    # 結巴斷詞
    words = jieba.cut(all_titles)
    
    # 過濾不要的常見字詞
    stop_words = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會"}
    filtered_words = " ".join([w for w in words if w not in stop_words and len(w) > 1])
    
    # 尋找 Ubuntu 的中文字型路徑
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
        
    try:
        wc = WordCloud(
            font_path=font_path,
            width=1000, 
            height=600,
            background_color='white',
            max_words=150,
            colormap='inferno' # 使用火焰顏色的主題，符合軍事動盪感
        )
        wordcloud_img = wc.generate(filtered_words)
        
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud_img, interpolation="bilinear")
        plt.axis("off")
        # 存檔成 wordcloud.png
        plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0)
        plt.close()
        print("✅ 文字雲產生成功！")
    except Exception as e:
        print(f"⚠️ 文字雲產生失敗: {e}")

# --- 主程式 ---
keyword = "軍事衝突"
old_news_list = get_existing_data()
existing_links = {n['link'] for n in old_news_list}

new_news = crawl_news(keyword, existing_links)
total_news = new_news + old_news_list

# 🌟 當有新新聞時，除了寫入 txt，順便重畫一張文字雲
if new_news:
    generate_wordcloud(total_news[:500])
    
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
