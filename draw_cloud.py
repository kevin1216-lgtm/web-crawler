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
    stop = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼"}
    words = " ".join([w for w in seg if w not in stop and len(w) > 1])

    font = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font):
        font = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    m_path = "mask.png"
    if os.path.exists(m_path):
        img = Image.open(m_path).convert("RGBA")
        base = Image.new("RGBA", img.size, (255, 255, 255, 255))
        base.paste(img, (0, 0), img)
        m_arr = np.array(base.convert("L"))
        m_arr = np.where(m_arr > 200, 255, 0)
    else:
        m_arr = None

    try:
        wc = WordCloud(
            font_path=font,
            mask=m_arr,
            width=1000,
            height=1000,             # 稍微拉高一點比例，讓圖形有更多空間
            background_color='white',
            max_words=3000,          # 🌟 暴力增加單字量，填滿縫隙
            max_font_size=40,        # 🌟 強制最大字體變小 (你可以自己微調這個數字，越小字越密)
            min_font_size=2,         # 允許字縮到極小
            relative_scaling=0.1,    # 🌟 降低大字霸佔空間的比例，讓版面充滿均勻的小字
            colormap='inferno',
            contour_width=1,         # 保留一點點史蒂夫的黑邊框
            contour_color='black'
        )
        out = wc.generate(words)
        plt.figure(figsize=(10, 10))
        plt.imshow(out, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0)
        plt.close()
        print("✅ 高密度文字雲產生成功！")
    except Exception as e:
        print(f"⚠️ 文字雲產生失敗: {e}")

if __name__ == "__main__":
    generate()
