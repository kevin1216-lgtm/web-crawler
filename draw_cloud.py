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
            height=800,
            background_color='white',
            max_words=1200,
            max_font_size=70,
            min_font_size=2,
            colormap='inferno',
            contour_width=1,
            contour_color='black'
        )
        out = wc.generate(words)
        plt.figure(figsize=(10, 8))
        plt.imshow(out, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0)
        plt.close()
    except:
        pass

if __name__ == "__main__":
    generate()
