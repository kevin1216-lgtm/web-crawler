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

    # 讀取文字檔內容
    with open(f_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    # 提取標題
    ptn = r"【.*?】(.*?)\n🔗"
    tags = re.findall(ptn, txt)
    if not tags:
        return

    all_t = " ".join(tags)
    
    # 結巴斷詞
    seg = jieba.cut(all_t)
    stop = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼", "表示", "認為", "可能", "已經"}
    words = " ".join([w for w in seg if w not in stop and len(w) > 1])

    # 字型設定
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
        # 單純的黑白二值化
        m_arr_1 = np.where(np.array(base1.convert("L")) > 200, 255, 0)
        
        try:
            # 🌟 提高解析度並開啟重複參數 (專治糊與字少) 🌟
            wc1 = WordCloud(
                font_path=font,
                mask=m_arr_1,
                width=2000,              # 提高畫布解析度
                height=2000,
                background_color='white',
                max_words=3000,          # 🌟 準備大量單字，填滿縫隙
                max_font_size=110,       # 最大石頭限制在 110，太大會破壞形狀
                min_font_size=2,         # 允許沙子縮到極小 (2)
                repeat=True,             # 🌟 魔法參數：無限重複使用小字把縫隙填滿！
                colormap='inferno',
                # 🌟 拿掉黑框：刪除 contour_width 和 contour_color
            )
            out1 = wc1.generate(words)
            
            plt.figure(figsize=(15, 15)) # 放大繪圖視窗
            # 🌟 更改顯示模式 (專治模糊)：使用 'nearest' 插值
            plt.imshow(out1, interpolation="nearest")
            plt.axis("off")
            # 🌟 DPI=300：強制輸出超清晰圖片
            plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 第一張圖 (史蒂夫) 產生成功！")
        except Exception as e:
            print(f"⚠️ 第一張圖產生失敗: {e}")

    # ==========================================
    # 🖼️ 第二張圖：星星頻率圖 (頻率越高字越大、無黑框)
    # ==========================================
    m_path_2 = "mask_heart.png" # 雖然檔名是 heart，但這裡會使用星星形狀，請上傳一張黑白星星剪影圖，命名為 mask_heart.png
    if os.path.exists(m_path_2):
        img2 = Image.open(m_path_2).convert("RGBA")
        base2 = Image.new("RGBA", img2.size, (255, 255, 255, 255))
        base2.paste(img2, (0, 0), img2)
        m_arr_2 = np.where(np.array(base2.convert("L")) > 200, 255, 0)
        
        try:
            # 🌟 星星也開啟重複參數，把角填滿 🌟
            wc2 = WordCloud(
                font_path=font,
                mask=m_arr_2,
                width=2000,              # 提高解析度
                height=2000,
                background_color='white',
                max_words=2500,          # 用大量小字把星星填滿
                max_font_size=180,       # 解除大字體封印，頻率高的詞會變超大
                min_font_size=2,
                repeat=True,             # 🌟 關鍵參數：把星星的角也填滿！
                relative_scaling=0.1,    # 🌟 降低大字霸佔空間的比例，讓版面充滿均勻的小字
                colormap='viridis'
            )
            out2 = wc2.generate(words)
            
            plt.figure(figsize=(15, 15))
            plt.imshow(out2, interpolation="nearest")
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
