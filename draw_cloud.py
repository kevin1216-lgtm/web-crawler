import os
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator # 確保有導入 ImageColorGenerator
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
    stop = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼", "表示", "認為", "可能", "已經", "這次", "我們", "目前"}
    words = " ".join([w for w in seg if w not in stop and len(w) > 1])

    font = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font):
        font = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    # ==========================================
    # 🖼️ 第一張圖：史蒂夫 (🌟 3D 立體色彩映射版 🌟)
    # ==========================================
    c_path_1 = "steve_color.png" 
    m_path_1 = "mask.png" # 遮罩
    if os.path.exists(c_path_1) and os.path.exists(m_path_1):
        color_img = Image.open(c_path_1).convert("RGBA")
        mask_img = Image.open(m_path_1).convert("RGBA")

        # 強制將兩張圖放大 5 倍並縮放到相同大小，保持高畫質與對齊
        scale = 5
        new_size = (mask_img.width * scale, mask_img.height * scale)
        color_img = color_img.resize(new_size, Image.LANCZOS)
        mask_img = mask_img.resize(new_size, Image.LANCZOS)

        # 建立白色底圖並貼上彩色史蒂夫 (處理透明背景)
        base1 = Image.new("RGBA", color_img.size, (255, 255, 255, 255))
        base1.paste(color_img, (0, 0), color_img)

        # 1️⃣ 產生用於「萃取顏色」的陣列
        color_array_1 = np.array(base1)

        # 2️⃣ 產生用於「決定形狀」的黑白遮罩陣列
        m_arr_1 = np.where(np.array(mask_img.convert("L")) > 240, 255, 0)

        try:
            # 調小字體，增加字數，提升細節
            wc1 = WordCloud(
                font_path=font, mask=m_arr_1, background_color='white',
                max_words=6000, max_font_size=120, min_font_size=4, 
                repeat=True
            )
            wc1.generate(words)

            # 🌟 終極魔法：根據原圖顏色重新上色 🌟
            image_colors_1 = ImageColorGenerator(color_array_1)
            wc1.recolor(color_func=image_colors_1)

            plt.figure(figsize=(20, 20))
            plt.imshow(wc1, interpolation="bilinear")
            plt.axis("off")
            plt.savefig("wordcloud_Steve.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 史蒂夫 3D 立體版產生成功！")
        except Exception as e:
            print(f"⚠️ 史蒂夫產生失敗: {e}")

    # ==========================================
    # 🖼️ 第二張圖：星星版 (維持不變)
    # ==========================================
    m_path_2 = "mask_star.png"
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
            plt.savefig("wordcloud_star.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 星星圖高畫質版產生成功！")
        except Exception as e:
            print(f"⚠️ 星星圖產生失敗: {e}")

    # ==========================================
    # 🖼️ 第三張圖：狗 (🌟 3D 立體色彩映射版 🌟)
    # ==========================================
    m_path_3 = "mask_dog.png" # 遮罩
    c_path_3 = "dog_color.png" # 彩色原圖
    if os.path.exists(m_path_3) and os.path.exists(c_path_3):
        mask_img_3 = Image.open(m_path_3).convert("RGBA")
        color_img_3 = Image.open(c_path_3).convert("RGBA")

        # 強制放大 5 倍並將彩色原圖縮放到遮罩大小
        scale = 5
        new_size_3 = (mask_img_3.width * scale, mask_img_3.height * scale)
        mask_img_3 = mask_img_3.resize(new_size_3, Image.LANCZOS)
        color_img_3 = color_img_3.resize(new_size_3, Image.LANCZOS)

        # 建立白色底圖貼上彩色狗 (處理透明背景)
        base3 = Image.new("RGBA", color_img_3.size, (255, 255, 255, 255))
        base3.paste(color_img_3, (0, 0), color_img_3)

        # 1️⃣ 產生用於萃取顏色的陣列
        color_array_3 = np.array(base3)

        # 2️⃣ 產生用於決定形狀的黑白遮罩陣列
        m_arr_3 = np.where(np.array(mask_img_3.convert("L")) > 240, 255, 0)

        try:
            # 調小字體，增加字數，提升立體細節
            wc3 = WordCloud(
                font_path=font, mask=m_arr_3, background_color='white',
                max_words=6000, max_font_size=150, min_font_size=4, 
                repeat=True
            )
            wc3.generate(words)

            # 🌟 終極魔法：根據原圖顏色重新上色 🌟
            image_colors_3 = ImageColorGenerator(color_array_3)
            wc3.recolor(color_func=image_colors_3)

            plt.figure(figsize=(20, 20))
            plt.imshow(wc3, interpolation="bilinear")
            plt.axis("off")
            # 🌟 記得設定存檔名稱：wordcloud_dog.png
            plt.savefig("wordcloud_dog.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 狗 3D 立體版產生成功！")
        except Exception as e:
            print(f"⚠️ 狗產生失敗: {e}")
    else:
        print("沒有找到 mask_dog.png 或 dog_color.png，跳過繪製。")

if __name__ == "__main__":
    generate()
