import os
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generate():
    f_path = 'result.txt'
    if not os.path.exists(f_path): return

    with open(f_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    ptn = r"【.*?】(.*?)\n🔗"
    tags = re.findall(ptn, txt)
    if not tags: return

    all_t = " ".join(tags)
    seg = jieba.cut(all_t)
    stop = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼", "表示", "認為", "可能", "已經", "這次", "目前", "我們"}
    words = " ".join([w for w in seg if w not in stop and len(w) > 1])

    font = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font):
        font = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    # 確保輸出資料夾存在
    os.makedirs("output", exist_ok=True)

    # ==========================================
    # 🖼️ 1. 史蒂夫 (對齊 masks/steve.png)
    # ==========================================
    c_path_1 = "masks/steve_color.png" 
    m_path_1 = "masks/steve.png" # 👈 對齊你的檔名
    if os.path.exists(c_path_1) and os.path.exists(m_path_1):
        color_img = Image.open(c_path_1).convert("RGBA")
        mask_img = Image.open(m_path_1).convert("RGBA")
        scale = 5
        new_size = (mask_img.width * scale, mask_img.height * scale)
        color_img = color_img.resize(new_size, Image.LANCZOS)
        mask_img = mask_img.resize(new_size, Image.LANCZOS)
        base1 = Image.new("RGBA", color_img.size, (255, 255, 255, 255))
        base1.paste(color_img, (0, 0), color_img)
        m_arr_1 = np.where(np.array(mask_img.convert("L")) > 240, 255, 0)
        
        wc1 = WordCloud(font_path=font, mask=m_arr_1, background_color='white',
                        max_words=6000, max_font_size=120, min_font_size=4, repeat=True)
        wc1.generate(words)
        wc1.recolor(color_func=ImageColorGenerator(np.array(base1)))
        plt.figure(figsize=(20, 20))
        plt.imshow(wc1, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("output/wordcloud_Steve.png", bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()
        print("✅ 史蒂夫 3D 版產生於 output/")

    # ==========================================
    # 🖼️ 2. 星星版 (對齊 masks/star.png)
    # ==========================================
    m_path_2 = "masks/star.png" # 👈 對齊你的檔名
    if os.path.exists(m_path_2):
        img2 = Image.open(m_path_2).convert("RGBA")
        img2 = img2.resize((img2.width * 5, img2.height * 5), Image.LANCZOS)
        m_arr_2 = np.where(np.array(img2.convert("L")) > 200, 255, 0)
        wc2 = WordCloud(font_path=font, mask=m_arr_2, background_color='white',
                        max_words=3000, max_font_size=400, min_font_size=8,
                        repeat=True, relative_scaling=0.1, colormap='viridis')
        wc2.generate(words)
        plt.figure(figsize=(20, 20))
        plt.imshow(wc2, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("output/wordcloud_star.png", bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()
        print("✅ 星星圖產生於 output/")

    # ==========================================
    # 🖼️ 3. 狼 (對齊 masks/wolf.png)
    # ==========================================
    m_path_3 = "masks/wolf.png" # 👈 對齊你的檔名
    c_path_3 = "masks/wolf_color.png"
    if os.path.exists(m_path_3) and os.path.exists(c_path_3):
        mask_img_3 = Image.open(m_path_3).convert("RGBA")
        color_img_3 = Image.open(c_path_3).convert("RGBA")
        scale = 5
        new_size_3 = (mask_img_3.width * scale, mask_img_3.height * scale)
        mask_img_3 = mask_img_3.resize(new_size_3, Image.LANCZOS)
        color_img_3 = color_img_3.resize(new_size_3, Image.LANCZOS)
        base3 = Image.new("RGBA", color_img_3.size, (255, 255, 255, 255))
        base3.paste(color_img_3, (0, 0), color_img_3)
        m_arr_3 = np.where(np.array(mask_img_3.convert("L")) > 240, 255, 0)
        
        wc3 = WordCloud(font_path=font, mask=m_arr_3, background_color='white',
                        max_words=6000, max_font_size=150, min_font_size=4, repeat=True)
        wc3.generate(words)
        wc3.recolor(color_func=ImageColorGenerator(np.array(base3)))
        plt.figure(figsize=(20, 20))
        plt.imshow(wc3, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("output/wordcloud_wolf.png", bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()
        print("✅ 狼 3D 版產生於 output/")

if __name__ == "__main__":
    generate()
