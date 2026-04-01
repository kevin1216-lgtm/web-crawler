import requests
from bs4 import BeautifulSoup
import datetime

def crawl_china_times(keyword):
    # 🌟 絕招：利用 Google News 的 RSS 功能，指定只搜尋中時新聞網 (site:chinatimes.com)
    url = f"https://news.google.com/rss/search?q=site:chinatimes.com+{keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    res = requests.get(url, headers=headers)
    results = []
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # Google News 的資料都放在 <item> 標籤裡面
        items = soup.find_all('item')
        
        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            
            if title_tag and link_tag:
                title = title_tag.text
                link = link_tag.text
                
                # Google News 抓出來的標題通常會附帶 "- 中時新聞網"，我們把它清掉讓版面好看點
                clean_title = title.split(" - ")[0]
                
                results.append(f"【中時】{clean_title}\n🔗 {link}")
                
        if len(results) == 0:
            results.append(f"⚠️ 【中時】連線成功，但 Google 尚未收錄「{keyword}」的最新新聞。")
    else:
        results.append(f"❌ 【中時】連線失敗 (狀態碼: {res.status_code})")
        
    return results 
    
def crawl_ltn(keyword):
    url = f"https://search.ltn.com.tw/list?keyword={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
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
                    
        if len(results) == 0:
            results.append(f"⚠️ 【自由】網頁連線成功，但目前沒有「{keyword}」的最新新聞。")
    else:
        results.append(f"❌ 【自由】連線失敗，可能被網站阻擋了 (狀態碼: {res.status_code})")
        
    return results

keyword = "軍事衝突"
all_news = []
all_news.extend(crawl_china_times(keyword))
all_news.extend(crawl_ltn(keyword))

output = f"🕒 自動更新時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
output += f"🔎 監控關鍵字：{keyword}\n"
output += "="*30 + "\n\n"
output += "\n\n".join(all_news)

# 把原本的 'w' 改成 'a' (Append 附加模式)
with open('result.txt', 'a', encoding='utf-8') as f:
    f.write(output)
    # 多加一行分隔線，讓每次更新的紀錄在視覺上隔開來
    f.write("\n" + "▼"*30 + "\n\n")
