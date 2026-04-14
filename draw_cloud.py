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

    # 提取標題
    ptn = r"【.*?】(.*?)\n🔗"
    tags = re.findall(ptn, txt)
    if not tags:
        return

    all_t = " ".join(tags)
    
    # 結巴斷詞
    seg = jieba.cut(all_t)
    stop = {"的", "了", "在", "是", "與", "和", "就", "也", "都", "不", "而", "有", "上", "將", "被", "會", "及", "等", "如何", "為何", "什麼", "表示", "認為", "可能", "已經", "這次", "表示", "認為", "可能", "已經"}
    words = " ".join([w for w in seg if w not in stop and len(w) > 1])

    # 字型設定
    font = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if not os.path.exists(font):
        font = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

    # ==========================================
    # 🖼️ 第一張圖：史蒂夫 (強制放大 5 倍版)
    # ==========================================
    m_path_1 = "mask.png"
    if os.path.exists(m_path_1):
        img1 = Image.open(m_path_1).convert("RGBA")
        
        # 🌟 終極殺招：強制將遮罩放大 5 倍！確保有足夠的像素畫高畫質文字
        # LANCZOS 插值可以確保放大後的圖片依然平滑
        scale = 5
        img1 = img1.resize((img1.width * scale, img1.height * scale), Image.LANCZOS)
        
        base1 = Image.new("RGBA", img1.size, (255, 255, 255, 255))
        base1.paste(img1, (0, 0), img1)
        # 單純的黑白二值化
        m_arr_1 = np.where(np.array(base1.convert("L")) > 200, 255, 0)
        
        try:
            # 開啟重複參數，暴力塞滿史蒂夫
            wc1 = WordCloud(
                font_path=font,
                mask=m_arr_1,
                background_color='white',
                max_words=4000,          # 🌟 準備大量單字，填滿縫隙
                max_font_size=250,       # 🌟 石頭也要跟著放大
                min_font_size=8,         # 沙子也要夠大
                repeat=True,             # 🌟 無限重複填滿
                colormap='inferno',
            )
            out1 = wc1.generate(words)
            
            plt.figure(figsize=(20, 20)) # 超大繪圖視窗
            # 更改顯示模式：使用 'bilinear' 讓邊緣在放大時更平滑
            plt.imshow(out1, interpolation="bilinear")
            plt.axis("off")
            # 🌟 DPI=300：強制輸出 4K 等級的超清晰圖片，絕對不糊！
            plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 第一張圖 (史蒂夫) 高畫質版產生成功！")
        except Exception as e:
            print(f"⚠️ 第一張圖產生失敗: {e}")

    # ==========================================
    # 🖼️ 第二張圖：星星 (強制放大 5 倍版)
    # ==========================================
    # 請上傳一張黑白星星剪影圖，命名為 mask_heart.png
    m_path_2 = "mask_heart.png"
    if os.path.exists(m_path_2):
        img2 = Image.open(m_path_2).convert("RGBA")
        
        # 🌟 終極殺招：同樣將星星強制放大 5 倍
        scale = 5
        img2 = img2.resize((img2.width * scale, img2.height * scale), Image.LANCZOS)
        
        base2 = Image.new("RGBA", img2.size, (255, 255, 255, 255))
        base2.paste(img2, (0, 0), img2)
        m_arr_2 = np.where(np.array(base2.convert("L")) > 200, 255, 0)
        
        try:
            # 星星也開啟重複參數，把角填滿，重點凸顯
            wc2 = WordCloud(
                font_path=font,
                mask=m_arr_2,
                background_color='white',
                max_words=3000,          # 暴力填滿星星
                max_font_size=400,       # 重點詞語可以無限放大
                min_font_size=8,
                repeat=True,             # 🌟 關鍵參數：把星星的角也填滿！
                relative_scaling=0.1,    # 🌟 降低大字霸佔空間的比例，讓版面充滿均勻的小字
                colormap='viridis'
            )
            out2 = wc2.generate(words)
            
            plt.figure(figsize=(20, 20))
            # 更改顯示模式：使用 'bilinear' 讓邊緣在放大時更平滑
            plt.imshow(out2, interpolation="bilinear")
            plt.axis("off")
            # 🌟 DPI=300：強制輸出 4K 等級的大圖，絕對清晰！
            plt.savefig("wordcloud_heart.png", bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            print("✅ 第二張圖 (星星頻率圖) 高畫質版產生成功！")
        except Exception as e:
            print(f"⚠️ 第二張圖產生失敗: {e}")
    else:
        print("沒有找到 mask_heart.png，跳過第二張圖的繪製。")

if __name__ == "__main__":
    generate()
