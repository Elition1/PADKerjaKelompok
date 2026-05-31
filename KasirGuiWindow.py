import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

TEST_VALUES = ["BARANG 1 - 50ML - RP50.000", "BARANG 2 - 50ML - RP50.000", 
               "BARANG 3 - 50ML - RP50.000"]

# font config
FONT_TYPE = "Times New Roman"
FONT_SIZE = 12
FONT_FOREGROUND = "#000000"

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

# Combo Box canvas kiri
START_X_COMBO_BOX = 20
START_Y_COMBO_BOX = 50
COMBO_BOX_CANVAS_KIRI_WIDTH = (LEFT_CANVAS_WIDTH - START_X_COMBO_BOX) - START_X_COMBO_BOX 

class KasirGuiWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MRmarket")
        self.geometry(f"{MAX_WIDTH}x{MAX_HEIGHT}+{START_WINDOW_X}+{START_WINDOW_Y}")
        self.resizable(False, False)
        self.overrideredirect(True)

        # bikin canvas objek
        self.canvasBlockLeft = None
        self.canvasBlockTop = None
        self.canvasBlockRight = None

    def window_initializer(self):
        # directory mencari img file untuk semua device
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "img", "icon.png")
        
        # menggunakan PIL image untuk membuat logo icon image
        pil_img = Image.open(icon_path)
        self.icon_image = ImageTk.PhotoImage(pil_img)
        
        # Untuk set icon image supaya bekerja di Windows, Linux, dan macOS
        self.wm_iconphoto(True, self.icon_image)

        # config background default dan transparan widget 10%
        self.config(bg = "#000000")
        self.attributes("-alpha", 10.0)

        # pembuatan style untuk manipulasi configurasi
        self.style = ttk.Style()
        self.style.theme_use("default")

    def draw_canvas(self):
        # Bikin Canvas atap
        self.canvasBlockTop = tk.Canvas(
            self,
            height = TOP_CANVAS_HEIGHT,
            bg = "#FFFFFF",
            highlightthickness = 0,
        )
        self.canvasBlockTop.pack(side = "top", fill = "x")

        # Bikin Canvas kiri
        self.canvasBlockLeft = tk.Canvas(
            self,
            width = LEFT_CANVAS_WIDTH,
            height = LEFT_CANVAS_HEIGHT,
            bg = "#8A8A75",
            highlightthickness = 0,
            
        )
        self.canvasBlockLeft.pack(side = "left")

        self.canvasBlockRight = tk.Canvas(
            self,
            height = RIGHT_CANVAS_HEIGHT,
            width = RIGHT_CANVAS_WIDTH,
            bg = "#3D3B3B",
            highlightthickness = 0
        )
        self.canvasBlockRight.pack(side = "right")        

    def draw_widget(self):
        self.comboBoxCanvasLeft = ttk.Combobox(
            self.canvasBlockLeft,
            font = (FONT_TYPE, FONT_SIZE),
            foreground = FONT_FOREGROUND,
            values = TEST_VALUES,
            state = "readonly"
        )
        self.comboBoxCanvasLeft.place(
            width = COMBO_BOX_CANVAS_KIRI_WIDTH,
            x = START_X_COMBO_BOX,
            y = START_Y_COMBO_BOX
        )
        self.comboBoxCanvasLeft.bind("<<ComboboxSelected>>", lambda e: self.comboBoxCanvasLeft.selection_clear())
        self.comboBoxCanvasLeft.bind("<FocusIn>", lambda e: self.comboBoxCanvasLeft.selection_clear())  
