import sys
import re
import tkinter as tk
import tkinter.font as tkfont

#▼コントロール定義
class ColorUnit(tk.Frame):
  def __init__(self, master, label_text, callback = None):
    super().__init__(master)
    
    #▼Scale（column=1）
    self.scale = tk.Scale(
      self,
      command = self.on_scale_change,
      from_ = 0, to = 255,
      highlightthickness=1,
      length = 156,
      orient = "horizontal",
      showvalue = False,
      sliderlength = 8,
      takefocus = True,
      bd = 0,
      troughcolor = "white",
      width = 16
    )
    self.scale.bind("<KeyPress-Up>", self.disable_keys)
    self.scale.bind("<KeyPress-Down>", self.disable_keys)
    self.scale.grid(row=0, column=1, sticky="ew")
    
    #▼Entry（column=2）
    self.textvar = tk.StringVar(value = 127) # 初期値
    self.textvar.trace_add("write", self.on_entry_change)
    self.entry = tk.Entry(
      self,
      width = 3,
      justify = "center",
      bd = 1,
      highlightthickness = 0,
      textvariable = self.textvar
    )
    self.on_entry_change()
    self.entry.bind("<KeyPress-Up>", self.increment)
    self.entry.bind("<KeyPress-Down>", self.decrement)
    self.entry.bind("<<Paste>>", self.on_paste)
    self.entry.grid(row=0, column=2, sticky="e")
    
    #▼Canvas（column=0）
    self.update_idletasks()
    canvas_h = max(self.scale.winfo_height(), self.entry.winfo_height())
    self.canvas = tk.Canvas(
      self,
      bg=master["bg"],
      bd=0,
      highlightthickness=0
    )
    
    # 仮テキスト作成
    label_text += "："
    text_id = self.canvas.create_text(0, 0, text=label_text)
    # 実際のフォント取得
    font = tkfont.Font(font=self.canvas.itemcget(text_id, "font"))
    # metrics取得
    ascent = font.metrics("ascent")
    descent = font.metrics("descent")
    text_h = ascent + descent
    text_w = font.measure(label_text)
    # 仮テキスト削除
    self.canvas.delete(text_id)
    
    canvas_w = text_w
    self.canvas.config(
      width=canvas_w,
      height=canvas_h
    )
    # textのx,y座標決める
    x = canvas_w / 2
    y = canvas_h / 2
    # 影作成
    text = self.canvas.create_text(
      x + 1, y + 1,
      text = label_text,
      fill = "silver"
    )
    # 文字作成
    text = self.canvas.create_text(
      x, y,
      text = label_text,
      fill = "black"
    )
    self.canvas.grid(row=0, column=0, sticky="w")
    
    # ユニット全体の余白はFrame側で統一
    self.config(padx=2, pady=2)
  
  @property
  def value(self):
    return int(self.entry.get())
  
  def disable_keys(self, event=None):
    return "break"
  
  def increment(self, event=None):
    num = int(self.entry.get())
    self.textvar.set(
      str(min(255, num + 1))
    )
  
  def decrement(self, event=None):
    num = int(self.entry.get())
    self.textvar.set(
      str(max(0, num - 1))
    )
  
  def on_scale_change(self, value):
    self.textvar.set(value)
    ChangeColor()
  
  def on_entry_change(self, *args):
    self.textvar.set(
      self.RangeRGB(self.entry.get())
    )
    self.scale.set(
      int(self.textvar.get())
    )
  
  def on_paste(self, event):
    # クリップボードから値取得
    try:
      paste_txt = event.widget.clipboard_get()
      txt = event.widget.get()
    except tk.TclError:
      return "break"
    
    # 選択範囲の文字列を削除
    if event.widget.selection_present():
      select_start = min(
        event.widget.index(tk.ANCHOR),
        event.widget.index(tk.INSERT)
      )
      select_end = max(
        event.widget.index(tk.ANCHOR),
        event.widget.index(tk.INSERT)
      )
      event.widget.delete(select_start, select_end)
      pos = select_start
    else:
      pos = event.widget.index(tk.INSERT)
    
    # クリップボードの文字を貼り付け
    event.widget.insert(pos, paste_txt)
    event.widget.icursor(pos + len(paste_txt))
    return "break"
  
  #▼Entryの内容を0-255へ置換
  def RangeRGB(self, txt):
    # 数値 (10進数以外の文字を削除)
    txt = re.sub(r"\D", "", txt)
    
    # RGB値の範囲
    if txt == "":
      txt = str(0)
    elif int(txt) >= 256:
      txt = str(255)
    
    return str(int(txt))

#▼母艦色変更
def ChangeColor():
  color = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
  root.config(bg=color)
  root.title(color)
  for unit in [r, g, b]:
    unit.config(bg=color)
    unit.canvas.config(bg=color)

#▼母艦作成
root = tk.Tk()
root.config(padx=3, pady=3) 
root.resizable(False, False)

#▼赤作成
r = ColorUnit(root, "赤")
r.pack()

#▼緑作成
g = ColorUnit(root, "緑")
g.pack()

#▼青作成
b = ColorUnit(root, "青")
b.pack()

#▼母艦浮上
ChangeColor()
root.mainloop()

sys.exit()
