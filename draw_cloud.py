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

    with open(f_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    ptn = r"【.*?】(.*?)\n🔗"
    tags = re.findall(ptn, txt)
    if not tags:
        return

    all_t = " ".join(tags)
    seg = jieba.cut(all_t)
    stop = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼", "表示", "認為", "可能", "已經", "這次"}
    words = " ".join([w for w in seg if w not in stop and len(w) > 1])

    font = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font):
        font = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    # ==========================================
    # 🖼️ 第一張圖：史蒂夫 (強制放大版)
    # ==========================================
    m_path_1 = "mask.png"
    if os.path.exists(m_path_1):
        img1 = Image.open(m_path_1).convert("RGBA")
        scale = 5
        img1 = img1.resize((img1.width * scale, img1.height * scale), Image.LANCZOS)
        
        base1 = Image.new("RGBA", img1.size, (255, 255, 255, 255))
        base1.paste(img1, (0, 0), img1)
        m_arr_1 = np.where(np.array(base1.convert("L")) > 200, 255, 0)
        
        try:
            wc1 = WordCloud(
                font_path=font, mask=m_arr_1, background_color='white',
                max_words=4000, max_font_size=250, min_font_size=8,
                repeat=True, colormap='inferno'
            )
            out1 = wc1.generate(words)
            plt.figure(figsize=(20, 20))
            plt.imshow(out1, interpolation="bilinear")
            plt.axis("off")
            plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 史蒂夫高畫質版產生成功！")
        except Exception as e:
            print(f"⚠️ 史蒂夫產生失敗: {e}")

    # ==========================================
    # 🖼️ 第二張圖：🌟 星星版 🌟 (全面改名 star)
    # ==========================================
    m_path_2 = "mask_star.png"   # 👈 這裡改成讀取 star
    if os.path.exists(m_path_2):
        img2 = Image.open(m_path_2).convert("RGBA")
        scale = 5
        img2 = img2.resize((img2.width * scale, img2.height * scale), Image.LANCZOS)
        
        base2 = Image.new("RGBA", img2.size, (255, 255, 255, 255))
        base2.paste(img2, (0, 0), img2)
        m_arr_2 = np.where(np.array(base2.convert("L")) > 200, 255, 0)
        
        try:
            wc2 = WordCloud(
                font_path=font, mask=m_arr_2, background_color='white',
                max_words=3000, max_font_size=400, min_font_size=8,
                repeat=True, relative_scaling=0.1, colormap='viridis'
            )
            out2 = wc2.generate(words)
            plt.figure(figsize=(20, 20))
            plt.imshow(out2, interpolation="bilinear")
            plt.axis("off")
            # 👈 這裡改成存成 wordcloud_star.png
            plt.savefig("wordcloud_star.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 星星圖高畫質版產生成功！")
        except Exception as e:
            print(f"⚠️ 星星圖產生失敗: {e}")
    else:
        print("沒有找到 mask_star.png，跳過繪製。")

if __name__ == "__main__":
    generate()
