import requests
from bs4 import BeautifulSoup
import datetime

keyword = "台灣"
url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
headers = {'User-Agent': 'Mozilla/5.0'}
cookies = {'over18': '1'}

response = requests.get(url, headers=headers, cookies=cookies)

# 準備要寫入檔案的內容
output_text = f"--- 抓取時間：{datetime.datetime.now()} ---\n"

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('div', class_='title')
    
    for t in titles:
        if t.a != None and keyword in t.a.text:
            output_text += f"發現關鍵字：{t.a.text}\n"
            output_text += f"連結：https://www.ptt.cc{t.a['href']}\n\n"

# 將結果覆寫存入 result.txt
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(output_text)
    
print("爬取完成，已存入 result.txt")
