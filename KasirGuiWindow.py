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

        # WINDOWS ONLY komen untuk nonaktifkan
        self.overrideredirect(True)

        # Logic Function
        self.logic = None

        # Variabel Function
        self.jumlahBarangVar = tk.StringVar()

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

        # Menghapus bagian atas window (Linux)
        # self.wm_attributes("-type", "splash")

        # config background default dan transparan window
        self.config(bg = config.BLACK)
        self.attributes("-alpha", 1)

        # pembuatan style untuk manipulasi configurasi
        self.style = ttk.Style()
        self.style.theme_use("default")

        # Manipulasi widget dengan tag ttk
        self.style.configure(
            "Keluar.TButton",
            font = (config.FONT_TYPE, config.FONT_BUTTON_SIZE),
            foreground = config.BLACK,
            background = config.WHITE,
            anchor = config.ANCHOR_CENTER,
            borderwidth = config.NON_BORDER
        )

        self.style.configure(
            "Tambah.TButton",
            font = (config.FONT_TYPE, config.FONT_BUTTON_SIZE),
            foreground = config.WHITE,
            background = config.GREEN,
            anchor = config.ANCHOR_CENTER,
            borderwidth = config.NON_BORDER
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
            foreground = config.WHITE,
            background = config.DARK_RED,
            anchor = config.ANCHOR_CENTER,
            borderwidth = config.NON_BORDER
        )

        self.style.map(
            "Hapus.TButton",
            background = [
                ('active', config.RED),
                ('pressed', config.WHITE),
                ('!disabled', config.DARK_RED)
            ]
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

        # Bikin Canvas kanan
        self.canvasBlockRight = tk.Canvas(
            self,
            height = config.RIGHT_CANVAS_HEIGHT,
            width = config.RIGHT_CANVAS_WIDTH,
            bg = config.CHARCOAL,
            highlightthickness = config.NON_BORDER_CANVAS
        )
        self.canvasBlockRight.pack(side = "right")        

    # Method pembuatan widget 
    def draw_widget(self):
        # buat combo box widget di canvas kiri
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

        self.jumlahBarangEntryBoxCanvasLeft = ttk.Entry(
            self.canvasBlockLeft,
            font = (config.FONT_TYPE, config.FONT_SIZE),
            foreground = config.BLACK,
            textvariable = self.jumlahBarangVar
        )
        self.jumlahBarangEntryBoxCanvasLeft.place(
            width = config.ENTRY_BOX_CANVAS_KIRI_WIDTH,
            x = config.START_X_ENTRY_BOX,
            y = config.START_Y_ENTRY_BOX
        )

        self.buttonKeluarTop = ttk.Button(
            self.canvasBlockTop,
            text = config.FONT_BUTTON_KELUAR_TEXT,
            style = "Keluar.TButton",
            cursor = config.CURSOR_HAND,
            command = self.logic.keluar_app
        )
        self.buttonKeluarTop.place(
            height = config.BUTTON_HEIGHT,
            width = config.BUTTON_WIDTH,
            x = config.START_X_BUTTON_KELUAR,
            y = config.START_Y_BUTTON_KELUAR
        )

        self.buttonTambahLeft = ttk.Button(
            self.canvasBlockLeft,
            text = config.FONT_BUTTON_TAMBAH_TEXT,
            style = "Tambah.TButton",
            cursor = config.CURSOR_HAND,
            command = self.logic.tambah_barang
        )
        self.buttonTambahLeft.place(
            height = config.BUTTON_HEIGHT,
            width = config.BUTTON_WIDTH,
            x = config.START_X_BUTTON_TAMBAH,
            y = config.START_Y_BUTTON_TAMBAH
        )

        self.buttonHapusRight = ttk.Button(
            self.canvasBlockRight,
            text = config.FONT_BUTTON_HAPUS_TEXT,
            style = "Hapus.TButton",
            cursor = config.CURSOR_HAND,
        )
        self.buttonHapusRight.place(
            height = config.BUTTON_HEIGHT,
            width = config.BUTTON_WIDTH,
            x = config.START_X_BUTTON_HAPUS,
            y = config.START_Y_BUTTON_HAPUS
        )

        self.listBoxCanvasKanan = tk.Listbox(
            self.canvasBlockRight,
            font = (config.FONT_TYPE, config.FONT_SIZE),
            background = config.WHITE,
            foreground = config.BLACK,
            borderwidth = config.NON_BORDER,
            cursor = "hand2",
        )
        self.listBoxCanvasKanan.place(
            width = config.LIST_BOX_CANVAS_KANAN_WIDTH,
            x = config.START_X_LIST_BOX_CANVAS_KANAN,
            y = config.START_Y_LIST_BOX_CANVAS_KIRI
        )
