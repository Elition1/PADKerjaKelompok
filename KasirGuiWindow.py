import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import ConfigGUI as config


class KasirGuiWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MRmarket")
        self.geometry(f"{config.MAX_WIDTH}x{config.MAX_HEIGHT}+{config.START_WINDOW_X}+{config.START_WINDOW_Y}")
        self.resizable(False, False)
        self.overrideredirect(True)

        # Logic Function
        self.logic = None

        # bikin canvas objek
        self.canvasBlockLeft = None
        self.canvasBlockTop = None
        self.canvasBlockRight = None

        # bikin widget
        self.comboBoxCanvasLeft = None


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
        self.config(bg = config.BLACK)
        self.attributes("-alpha", 0.90)

        # pembuatan style untuk manipulasi configurasi
        self.style = ttk.Style()

        self.style.configure(
            "Tambah.TButton",
            font = (config.FONT_TYPE, config.FONT_BUTTON_SIZE),
            foreground = config.WHITE,
            background = config.GREEN,
            anchor = "center"
        )

        self.style.map(
            "Tambah.TButton",
            background = [
                ('active', config.LIGHT_GREEN),
                ('pressed', config.WHITE),
                ('!disabled', config.GREEN)
            ]
        )

        self.style.configure(
            "Hapus.TButton",
            font = (config.FONT_TYPE, config.FONT_BUTTON_SIZE),
            foreground = config.WHITE
        )

    def draw_canvas(self):
        # Bikin Canvas atap
        self.canvasBlockTop = tk.Canvas(
            self,
            height = config.TOP_CANVAS_HEIGHT,
            bg = config.WHITE,
            highlightthickness = config.NON_BORDER_CANVAS,
        )
        self.canvasBlockTop.pack(side = "top", fill = "x")

        # Bikin Canvas kiri
        self.canvasBlockLeft = tk.Canvas(
            self,
            width = config.LEFT_CANVAS_WIDTH,
            height = config.LEFT_CANVAS_HEIGHT,
            bg = config.OLIVE_GREEN,
            highlightthickness = config.NON_BORDER_CANVAS,
            
        )
        self.canvasBlockLeft.pack(side = "left")

        self.canvasBlockRight = tk.Canvas(
            self,
            height = config.RIGHT_CANVAS_HEIGHT,
            width = config.RIGHT_CANVAS_WIDTH,
            bg = config.CHARCOAL,
            highlightthickness = config.NON_BORDER_CANVAS
        )
        self.canvasBlockRight.pack(side = "right")        

    def draw_widget(self):
        self.comboBoxCanvasLeft = ttk.Combobox(
            self.canvasBlockLeft,
            font = (config.FONT_TYPE, config.FONT_SIZE),
            foreground = config.BLACK,
            values = config.TEST_VALUES,
            state = "readonly"
        )
        self.comboBoxCanvasLeft.place(
            width = config.COMBO_BOX_CANVAS_KIRI_WIDTH,
            x = config.START_X_COMBO_BOX,
            y = config.START_Y_COMBO_BOX
        )
        self.comboBoxCanvasLeft.bind("<<ComboboxSelected>>", self.logic.non_background_effects)
        self.comboBoxCanvasLeft.bind("<FocusIn>", self.logic.non_background_effects)

        self.buttonTambahLeft = ttk.Button(
            self.canvasBlockLeft,
            text = config.FONT_BUTTON_TAMBAH_TEXT,
            style = "Tambah.TButton"
        )
        self.buttonTambahLeft.place(
            height = config.BUTTON_TAMBAH_HEIGHT,
            width = config.BUTTON_TAMBAH_WIDTH,
            x = config.START_X_BUTTON_TAMBAH,
            y = config.START_Y_BUTTON_TAMBAH
        )

        self.buttonHapusRight = ttk.Button(
            self.canvasBlockRight,
            text = config.FONT_BUTTON_HAPUS_TEXT,

        )
