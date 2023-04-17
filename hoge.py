### インポート
import tkinter
from PIL import Image, ImageTk

### 画像ロード
image: Image = Image.open("S__26771538.jpg")

### サイズ縮小
w_size = int(image.width / 4)
h_size = int(image.height / 4)

### キャンバス作成
canvas = tkinter.Canvas(width=w_size, height=h_size)

### PhotoImage変換
tk_image = ImageTk.PhotoImage(image=image.resize((w_size, h_size)))

### 画像描画
canvas.create_image(0, 0, anchor="nw", image=tk_image)

### キャンバス表示
canvas.pack()

### イベントループ
canvas.mainloop()
