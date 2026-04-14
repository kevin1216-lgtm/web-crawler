import os
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator # 🌟 新增導入 ImageColorGenerator
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
    # 🖼️ 第一張圖：史蒂夫 (🌟 3D 立體色彩映射版 🌟)
    # ==========================================
    m_path_1 = "steve_color.png" # 👈 改為讀取你新上傳的「彩色版」史蒂夫
    if os.path.exists(m_path_1):
        color_img = Image.open(m_path_1).convert("RGBA")
        
        # 放大 5 倍保持高畫質
        scale = 5
        color_img = color_img.resize((color_img.width * scale, color_img.height * scale), Image.LANCZOS)
        
        # 建立白色底圖並貼上史蒂夫 (處理透明背景)
        base1 = Image.new("RGBA", color_img.size, (255, 255, 255, 255))
        base1.paste(color_img, (0, 0), color_img)
        
        # 1️⃣ 產生用於「萃取顏色」的陣列
        color_array = np.array(base1)
        
        # 2️⃣ 產生用於「決定形狀」的黑白遮罩陣列
        m_arr_1 = np.where(np.array(base1.convert("L")) > 240, 255, 0)
        
        try:
            # 🌟 為了呈現 3D 細節，稍微調小字體，讓「像素點(文字)」更密集
            wc1 = WordCloud(
                font_path=font, mask=m_arr_1, background_color='white',
                max_words=6000, max_font_size=120, min_font_size=4, 
                repeat=True
                # 這裡先把 colormap 拿掉，因為我們要用原圖顏色
            )
            # 先畫出形狀
            wc1.generate(words)
            
            # 🌟 終極魔法：根據原圖顏色重新上色 🌟
            image_colors = ImageColorGenerator(color_array)
            wc1.recolor(color_func=image_colors)
            
            plt.figure(figsize=(20, 20))
            plt.imshow(wc1, interpolation="bilinear") # 注意這裡改成 wc1
            plt.axis("off")
            plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0, dpi=300)
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
    else:
        print("沒有找到 mask_star.png，跳過繪製。")

if __name__ == "__main__":
    generate()
