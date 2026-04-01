import requests
from bs4 import BeautifulSoup
import datetime

def crawl_china_times(keyword):
    url = f"https://www.chinatimes.com/search/{keyword}?chdtv"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    results = []
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.find_all('h3')
        for item in items:
            a_tag = item.find('a')
            if a_tag and a_tag.get('href'):
                title = a_tag.text.strip()
                link = a_tag.get('href')
                
                if not link.startswith('http'):
                    link = 'https://www.chinatimes.com' + link
                    
                if keyword in title:
                    results.append(f"【中時】{title}\n🔗 {link}")
                    
        if len(results) == 0:
            results.append(f"⚠️ 【中時】網頁連線成功，但目前沒有「{keyword}」的最新新聞。")
    else:
        results.append(f"❌ 【中時】連線失敗，可能被網站阻擋了 (狀態碼: {res.status_code})")
        
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

with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(output)
