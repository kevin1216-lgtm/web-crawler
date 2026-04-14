import os
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generate():
    f_path = 'result.txt'
    if not os.path.exists(f_path):
        return

    # 讀取新聞文字
    with open(f_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    ptn = r"【.*?】(.*?)\n🔗"
    tags = re.findall(ptn, txt)
    if not tags:
        return

    all_t = " ".join(tags)
    seg = jieba.cut(all_t)
    stop = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼", "表示", "認為", "可能", "已經"}
    words = " ".join([w for w in seg if w not in stop and len(w) > 1])

    font = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font):
        font = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    # ==========================================
    # 🖼️ 第一張圖：史蒂夫 (精細輪廓、高密度)
    # ==========================================
    m_path_1 = "mask.png"
    if os.path.exists(m_path_1):
        img1 = Image.open(m_path_1).convert("RGBA")
        base1 = Image.new("RGBA", img1.size, (255, 255, 255, 255))
        base1.paste(img1, (0, 0), img1)
        m_arr_1 = np.where(np.array(base1.convert("L")) > 200, 255, 0)
        
        try:
            wc1 = WordCloud(
                font_path=font, mask=m_arr_1, width=2000, height=2000,
                background_color='white', max_words=2000, max_font_size=110, min_font_size=2,
                repeat=True, colormap='inferno', contour_width=2, contour_color='black'
            )
            out1 = wc1.generate(words)
            plt.figure(figsize=(15, 15))
            plt.imshow(out1, interpolation="bilinear")
            plt.axis("off")
            plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 第一張圖 (史蒂夫) 產生成功！")
        except Exception as e:
            print(f"⚠️ 第一張圖產生失敗: {e}")

    # ==========================================
    # 🖼️ 第二張圖：星星圖 (頻率越大字越大、無黑框)
    # ==========================================
    m_path_2 = "mask_star.png"
    if os.path.exists(m_path_2):
        img2 = Image.open(m_path_2).convert("RGBA")
        base2 = Image.new("RGBA", img2.size, (255, 255, 255, 255))
        base2.paste(img2, (0, 0), img2)
        m_arr_2 = np.where(np.array(base2.convert("L")) > 200, 255, 0)
        
        try:
            wc2 = WordCloud(
                font_path=font, mask=m_arr_2, width=1500, height=1500,
                background_color='white', 
                max_words=500,        # 字數少一點，讓重點更突出
                max_font_size=250,    # 最大字體調超級大
                min_font_size=4,
                repeat=False,         # 不重複塞字，呈現大字重點感
                colormap='viridis'    # 換另一種顏色風格做區分
            )
            out2 = wc2.generate(words)
            plt.figure(figsize=(12, 12))
            plt.imshow(out2, interpolation="bilinear")
            plt.axis("off")
            plt.savefig("wordcloud_heart.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 第二張圖 (星星頻率圖) 產生成功！")
        except Exception as e:
            print(f"⚠️ 第二張圖產生失敗: {e}")
    else:
        print("沒有找到 mask_heart.png，跳過第二張圖的繪製。")

if __name__ == "__main__":
    generate()
