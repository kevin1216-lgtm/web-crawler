import os
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator # 🌟 新增 ImageColorGenerator
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
        # 🌟 1. 裝甲級遮罩處理與內部挖空 (專治臉型與模糊) 🌟
        img = Image.open(m_path).convert("RGBA")
        
        # 將史蒂夫圖片與白底結合 (處理透明背景)
        base = Image.new("RGBA", img.size, (255, 255, 255, 255))
        base.paste(img, (0, 0), img)
        processed_img = base.convert("RGB") # 保留顏色
        
        # 製作黑白遮罩用於排版 (史蒂夫區域為黑，背景為白)
        m_arr = np.array(base.convert("L"))
        m_arr = np.where(m_arr > 200, 255, 0)
        
        # 🌟 2. 給史蒂夫一張臉 (手動將臉部特徵區域變為白色，不可塞字) 🌟
        # 這需要根據你圖片的解析度手動微調坐標。以下是一組預估坐標。
        # [y, x] = y坐標從 y1:y2，x坐標從 x1:x2
        # 你需要根據產生的圖片效果，反覆調整這三個區域。
        h, w_img = m_arr.shape
        eyes_y1, eyes_y2 = int(h*0.1), int(h*0.18) # 預估眼睛 Y 坐標
        mouth_y1, mouth_y2 = int(h*0.22), int(h*0.25) # 預估嘴巴 Y 坐標
        l_eye_x1, l_eye_x2 = int(w_img*0.3), int(w_img*0.45) # 預估左眼 X 坐標
        r_eye_x1, r_eye_x2 = int(w_img*0.55), int(w_img*0.7) # 預估右眼 X 坐標
        mouth_x1, mouth_x2 = int(w_img*0.35), int(w_img*0.65) # 預估嘴巴 X 坐標
        
        # 將眼睛和嘴巴區域手動挖白
        m_arr[eyes_y1:eyes_y2, l_eye_x1:l_eye_x2] = 255 # 左眼
        m_arr[eyes_y1:eyes_y2, r_eye_x1:r_eye_x2] = 255 # 右眼
        m_arr[mouth_y1:mouth_y2, mouth_x1:mouth_x2] = 255 # 嘴巴

    else:
        print(f"找不到遮罩 {m_path}，將使用長方形。")
        m_arr = None
        processed_img = None

    try:
        # 🌟 3. 提高解析度並開啟重複參數 (專治十字鎬看不見) 🌟
        wc = WordCloud(
            font_path=font,
            mask=m_arr,
            width=2000,              # 提高解析度，讓十字鎬等細窄區域能塞字
            height=2000,
            background_color='white',
            max_words=1000,          # 適量單字，錯落有致
            max_font_size=150,       
            min_font_size=4,
            repeat=True,             # 🌟 魔法參數：無限重複使用小字把縫隙填滿！
        )
        out = wc.generate(words)
        
        # 🌟 4. 使用顏色遮罩 (讓字的顏色跟衣服、臉一樣) 🌟
        if processed_img:
            color_model = ImageColorGenerator(processed_img)
            # 將顏色套用到生成的文字雲
            out = out.recolor(color_func=color_model)

        plt.figure(figsize=(10, 10))
        # 🌟 5. 更改顯示模式 (專治模糊) 🌟
        # 使用 'nearest' 插值，確保文字邊緣清晰銳利
        plt.imshow(out, interpolation="nearest")
        plt.axis("off")
        # 提高存檔解析度
        plt.savefig("wordcloud.png", bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()
        print("✅ 儀表板級清晰、有臉型史蒂夫文字雲產生成功！")
    except Exception as e:
        print(f"⚠️ 文字雲產生失敗: {e}")

if __name__ == "__main__":
    generate()
