import os
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np # 新增 numpy 庫
from PIL import Image # 新增 Image 庫

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

    # --- 🌟 新增步驟：準備形狀遮罩 🌟 ---
    # 請確保您在 GitHub 儲存庫的根目錄下上傳了一個名為 'mask.png' 的黑白遮罩圖片。
    # 您可以使用地圖、武器、或其他任何形狀的黑白剪影。
    mask_path = "mask.png"
    if not os.path.exists(mask_path):
        print(f"找不到遮罩圖片 {mask_path}。將使用默認長方形。")
        mask_array = None
    else:
        # 使用 PIL 加載圖像，並將其轉換為 numpy 數組。
        mask_image = Image.open(mask_path)
        mask_array = np.array(mask_image)
        # 對於 wordcloud 庫，純白色區域代表“不可放置文字”。
        # 如果您的圖片背景不是純白色 (255, 255, 255)，您可能需要進行一些處理。
        # 最簡單的方法是使用二值化或將所有大於某個閾值的像素設為純白。
        mask_array[mask_array > 200] = 255 # 簡單的處理方法

    # 6. 畫圖並存檔
    try:
        wc = WordCloud(
            font_path=font_path,
            mask=mask_array, # 🌟 關鍵參數：傳入遮罩數組 🌟
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
        print("✅ 文字雲產生成功！(使用特定形狀)")
    except Exception as e:
        print(f"⚠️ 文字雲產生失敗: {e}")

if __name__ == "__main__":
    generate_wordcloud()
