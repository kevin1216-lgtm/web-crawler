import os
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generate_wordcloud():
    # 1. 確認文字檔
    if not os.path.exists('result.txt'):
        print("找不到 result.txt，無法產生文字雲。")
        return

    # 2. 讀取內容
    with open('result.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"【.*?】(.*?)\n🔗"
    titles = re.findall(pattern, content)

    if not titles:
        print("沒有找到任何新聞標題。")
        return

    all_titles = " ".join(titles)
    
    # 3. 結巴斷詞
    words = jieba.cut(all_titles)
    stop_words = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼"}
    filtered_words = " ".join([w for w in words if w not in stop_words and len(w) > 1])

    # 4. 字型設定
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    # 🌟 5. 裝甲級遮罩處理 (專治透明背景) 🌟
    mask_path = "mask.png"
    if not os.path.exists(mask_path):
        print(f"找不到遮罩 {mask_path}，將使用長方形。")
        mask_array = None
    else:
        try:
            # 讀取圖片並強制轉換為帶有透明通道的 RGBA 模式
            img = Image.open(mask_path).convert("RGBA")
            # 建立一張跟原圖一樣大的「純白底圖」
            bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
            # 把史蒂夫貼到白底圖上 (透明的部分就會被白色填滿)
            bg.paste(img, (0, 0), img)
            # 轉成灰階
            gray_img = bg.convert("L")
            mask_array = np.array(gray_img)
            # 終極二值化：把淺色(背景)變成純白(255)，把深色(史蒂夫)變成純黑(0)
            mask_array = np.where(mask_array > 200, 255, 0)
        except Exception as e:
            print(f"處理遮罩圖片時發生錯誤: {e}")
            mask_array = None

    # 6. 畫圖並存檔
    try:
        wc = WordCloud(
            font_path=font_path,
            mask=mask_array,         # 套用剛剛處理好的史蒂夫遮罩
            width=1000,
            height=600,
            background_color='white',
            max_words=300,           # 稍微增加字數，讓史蒂夫的輪廓更密實
            colormap='inferno',
            contour_width=2,         # 加上邊框線
            contour_color='black'    # 邊框線設為黑色，讓形狀更清晰
        )
        wordcloud_img = wc.generate(filtered_words)

        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud_img, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0)
        plt.close()
        print("✅ 文字雲產生成功！(史蒂夫形狀已套用)")
    except Exception as e:
        print(f"⚠️ 文字雲產生失敗: {e}")

if __name__ == "__main__":
    generate_wordcloud()
