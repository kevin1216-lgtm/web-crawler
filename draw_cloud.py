import os
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud():
    # 1. 確認有沒有文字檔可以讀
    if not os.path.exists('result.txt'):
        print("找不到 result.txt，無法產生文字雲。")
        return

    # 2. 讀取文字檔內容
    with open('result.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. 把新聞標題全部抓出來 (利用正規表達式)
    pattern = r"【.*?】(.*?)\n🔗"
    titles = re.findall(pattern, content)

    if not titles:
        print("沒有找到任何新聞標題。")
        return

    all_titles = " ".join(titles)
    
    # 4. 結巴斷詞與過濾
    words = jieba.cut(all_titles)
    stop_words = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等"}
    filtered_words = " ".join([w for w in words if w not in stop_words and len(w) > 1])

    # 5. 設定中文字型路徑
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    # 6. 畫圖並存檔
    try:
        wc = WordCloud(
            font_path=font_path,
            width=1000,
            height=600,
            background_color='white',
            max_words=150,
            colormap='inferno'
        )
        wordcloud_img = wc.generate(filtered_words)

        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud_img, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0)
        plt.close()
        print("✅ 文字雲產生成功！(獨立模組執行)")
    except Exception as e:
        print(f"⚠️ 文字雲產生失敗: {e}")

if __name__ == "__main__":
    generate_wordcloud()
