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
    stop = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼", "表示", "認為", "可能", "已經"}
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
            height=1000,
            background_color='white',
            max_words=3000,          # 🌟 秘訣1：倒進海量的沙子(小字)去填滿所有縫隙
            max_font_size=90,        # 🌟 秘訣2：最大字體壓制在90(中等石頭)，確保大字能突顯，但不會卡住手臂
            min_font_size=2,         # 允許產生極小的字來填補邊緣
            relative_scaling=0.5,    # 🌟 秘訣3：保持頻率與大小的黃金比例
            repeat=True,             # 🌟 秘訣4：如果字不夠塞滿史蒂夫，允許重複使用詞彙！保證100%填滿！
            colormap='inferno'
            # 黑框已經被我們徹底刪除了！
        )
        out = wc.generate(words)
        plt.figure(figsize=(10, 10))
        plt.imshow(out, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0)
        plt.close()
        print("✅ 飽滿型頻率文字雲產生成功！")
    except Exception as e:
        print(f"⚠️ 文字雲產生失敗: {e}")

if __name__ == "__main__":
    generate()
