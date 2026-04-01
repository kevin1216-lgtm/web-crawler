import requests
from bs4 import BeautifulSoup
import datetime

def crawl_china_times(keyword):
    # 中時搜尋網址
    url = f"https://www.chinatimes.com/search/{keyword}?chdtv"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    results = []
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # 抓取搜尋結果的標題區塊
        items = soup.find_all('h3', class_='title')
        for item in items:
            title = item.text.strip()
            link = item.find('a')['href']
            results.append(f"【中時】{title}\n🔗 {link}")
    return results

def crawl_ltn(keyword):
    # 自由時報搜尋網址
    url = f"https://search.ltn.com.tw/list?keyword={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    results = []
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # 自由時報搜尋結果放在特定的 ul > li 裡
        items = soup.select('ul.list > li')
        for item in items:
            a_tag = item.find('a', class_='tit')
            if a_tag:
                title = a_tag.text.strip()
                link = a_tag['href']
                results.append(f"【自由】{title}\n🔗 {link}")
    return results

# 主程式
keyword = "軍事衝突"
print(f"開始搜尋關鍵字：{keyword}")

all_news = []
all_news.extend(crawl_china_times(keyword))
all_news.extend(crawl_ltn(keyword))

# 格式化輸出內容
output_content = f"🕒 更新時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
output_content += f"🔎 關鍵字：{keyword}\n"
output_content += "="*30 + "\n"

if all_news:
    output_content += "\n\n".join(all_news)
else:
    output_content += "目前未找到相關新聞。"

# 儲存結果
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(output_content)

print("✅ 任務完成，結果已存入 result.txt")
