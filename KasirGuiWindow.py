import tkinter as tk
import os
from PIL import Image, ImageTk

# kordinat bikin window
START_WINDOW_X = 540
START_WINDOW_Y = 200

# besar window
MAX_WIDTH = 920
MAX_HEIGHT = 800

# window canvas atas
TOP_CANVAS_HEIGHT = 100

# window canvas kanan
RIGHT_CANVAS_WIDTH = 460
RIGHT_CANVAS_HEIGHT = MAX_HEIGHT - TOP_CANVAS_HEIGHT

# window canvas kiri
LEFT_CANVAS_WIDTH = MAX_WIDTH - RIGHT_CANVAS_WIDTH
LEFT_CANVAS_HEIGHT = MAX_HEIGHT - TOP_CANVAS_HEIGHT


class KasirGuiWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MRmarket")
        self.geometry(f"{MAX_WIDTH}x{MAX_HEIGHT}+{START_WINDOW_X}+{START_WINDOW_Y}")
        self.resizable(False, False)
        self.overrideredirect(True)

        # bikin canvas objek
        self.canvasblockleft = None
        self.canvasblocktop = None
        self.canvasblockright = None

    def window_initializer(self):
        # directory mencari img file untuk semua device
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "img", "icon.png")
        
        # menggunakan PIL image untuk membuat logo icon image
        pil_img = Image.open(icon_path)
        self.icon_image = ImageTk.PhotoImage(pil_img)
        
        # Untuk set icon image supaya bekerja di Windows, Linux, dan macOS
        self.wm_iconphoto(True, self.icon_image)

        self.config(bg="#9155a5")

    def draw_canvas(self):
        # Bikin Canvas atap
        self.canvasblocktop = tk.Canvas(
            self,
            height = TOP_CANVAS_HEIGHT,
            bg = "#FFFFFF",
            highlightthickness = 0,
        )
        self.canvasblocktop.pack(side = "top", fill = "x")

        # Bikin Canvas kiri
        self.canvasblockleft = tk.Canvas(
            self,
            width = LEFT_CANVAS_WIDTH,
            height = LEFT_CANVAS_HEIGHT,
            bg = "#8A8A75",
            highlightthickness = 0,
            
        )
        self.canvasblockleft.pack(side = "left")

        self.canvasblockright = tk.Canvas(
            self,
            height = RIGHT_CANVAS_HEIGHT,
            width = RIGHT_CANVAS_WIDTH,
            bg = "#3D3B3B",
            highlightthickness = 0
        )
        self.canvasblockright.pack(side = "right")        