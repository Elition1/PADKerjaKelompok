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

        # Variabel Function
        self.jumlahBarangVar = tk.StringVar()

        # Inisialisasi Objek Canvas
        self.canvasBlockLeft = None
        self.canvasBlockTop = None
        self.canvasBlockRight = None
        self.footerCanvas = None

        # Inisialisasi Objek Widget
        self.comboBoxCanvasLeft = None
        self.frameCanvasKanan = None
        self.jumlahBarangEntryBoxCanvasLeft = None
        self.labelFooterTanggal = None
        self.labelInputJumlah = None
        self.labelNamaBarang = None
        self.labelTotal = None
        self.buttonHapusRight = None
        self.buttonKeluarTop = None
        self.buttonTambahLeft = None
        self.buttonPembayaranRight = None
        self.buttonResetRight = None
        self.labelNamaBarang = None
        self.treeViewCanvasKanan = None

        # Logic Function Linker
        self.logic = None

    def window_initializer(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "img", "MRromusha.png")
        
        # Load icon jika folder img dan filenya tersedia
        if os.path.exists(icon_path):
            pil_img = Image.open(icon_path)
            img_path = Image.open(icon_path)
            self.icon_image = ImageTk.PhotoImage(pil_img)
            self.wm_iconphoto(True, self.icon_image)
            self.logo = img_path.resize((config.MAX_WIDTH_LOGO, config.MAX_HEIGHT_LOGO))
            self.tlogo = ImageTk.PhotoImage(self.logo)
        

        # menghapuskan bagian atas window (OS WINDOWS ONLY)
        self.overrideredirect(True)

        # FIX SECURITY EXCEPTION: Hanya hilangkan border atas jika berjalan di LINUX
        if os.name != 'nt':
            self.wm_attributes("-type", "splash")

        self.config(bg = config.BLACK)
        self.attributes("-alpha", 1)

        self.style = ttk.Style()
        self.style.theme_use("default")

        # Konfigurasi Style Button Tema Kelompok
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
                ('pressed', config.WHITE)
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
                ('pressed', config.WHITE)
            ]
        )

        self.style.configure(
            "Pembayaran.TButton",
            font = (config.FONT_TYPE, config.FONT_BUTTON_SIZE),
            foreground = config.WHITE,
            background = config.DARK_BLUE,
            anchor = config.ANCHOR_CENTER,
            borderwidth = config.NON_BORDER
        )

        self.style.configure(
            "Reset.TButton",
            font = (config.FONT_TYPE, config.FONT_BUTTON_SIZE),
            foreground = config.WHITE,
            background = config.PINKISH,
            anchor = config.ANCHOR_CENTER,
            borderwidth = config.NON_BORDER
        )
        self.style.map(
            "Reset.TButton",
            background = [('active', config.RED)]
        )

        self.style.configure(
            "Treeview",
            font = (config.FONT_TYPE, config.FONT_BUTTON_SIZE),
            background = config.WHITE
        )

    def draw_canvas(self):
        self.canvasBlockTop = tk.Canvas(
            self,
            height = config.TOP_CANVAS_HEIGHT, 
            bg = config.WHITE, 
            highlightthickness = config.NON_BORDER_CANVAS
        )
        self.canvasBlockTop.pack(
            side = "top",
            fill = "x"
        )
        
        self.footerCanvas = tk.Canvas(
            self, 
            height = config.BOTTOM_CANVAS_HEIGHT,
            bg = config.WHITE,
            highlightthickness = config.NON_BORDER_CANVAS
        )
        self.footerCanvas.pack(
            side = "bottom",
            fill = "x"
        )

        self.canvasBlockLeft = tk.Canvas(
            self,
            width = config.LEFT_CANVAS_WIDTH,
            height = config.LEFT_CANVAS_HEIGHT,
            bg = config.OLIVE_GREEN,
            highlightthickness = config.NON_BORDER_CANVAS
        )
        self.canvasBlockLeft.pack(
            side = "left"
        )

        self.canvasBlockRight = tk.Canvas(
            self,
            height = config.RIGHT_CANVAS_HEIGHT,
            width = config.RIGHT_CANVAS_WIDTH,
            bg = config.CHARCOAL,
            highlightthickness = config.NON_BORDER_CANVAS
        )
        self.canvasBlockRight.pack(
            side = "right"
        )        

    def draw_widget(self):
        self.comboBoxCanvasLeft = ttk.Combobox(
            self.canvasBlockLeft, 
            font = (config.FONT_TYPE, config.FONT_SIZE), 
            foreground = config.BLACK, 
            state = "readonly"
        )
        self.comboBoxCanvasLeft.place(
            width = config.COMBO_BOX_CANVAS_KIRI_WIDTH, 
            x = config.START_X_COMBO_BOX, 
            y = config.START_Y_COMBO_BOX
        )
    
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
        )
        self.buttonKeluarTop.place(
            height = config.BUTTON_HEIGHT,
            width = config.BUTTON_KELUAR_ATAS_WIDTH,
            x = config.START_X_BUTTON_KELUAR,
            y = config.START_Y_BUTTON_KELUAR
        )

        # FIX: Mengosongkan command agar diikat paksa secara bersih lewat Runner setelah widget lahir
        self.buttonTambahLeft = ttk.Button(
            self.canvasBlockLeft,
            text = config.FONT_BUTTON_TAMBAH_TEXT,
            style = "Tambah.TButton",
            cursor = config.CURSOR_HAND
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
            cursor = config.CURSOR_HAND
        )
        self.buttonHapusRight.place(
            height = config.BUTTON_HEIGHT,
            width = config.BUTTON_WIDTH,
            x = config.START_X_BUTTON_HAPUS,
            y = config.START_Y_BUTTON_HAPUS
        )

        # FIX: Mengosongkan command agar diikat paksa secara bersih lewat Runner setelah widget lahir
        self.buttonPembayaranRight = ttk.Button(
            self.canvasBlockRight,
            text = config.FONT_BUTTON_PEMBAYARAN_TEXT,
            style = "Pembayaran.TButton",
            cursor = config.CURSOR_HAND
        )
        self.buttonPembayaranRight.place(
            width = config.BUTTON_WIDTH,
            height = config.BUTTON_HEIGHT,
            x = config.START_X_BUTTON_PEMBAYARAN,
            y = config.START_Y_BUTTON_PEMBAYARAN
        )

        self.buttonResetRight = ttk.Button(
            self.canvasBlockRight,
            text = config.FONT_BUTTON_RESET_TEXT,
            style = "Reset.TButton",
            cursor = config.CURSOR_HAND
        )
        self.buttonResetRight.place(
            width = config.BUTTON_WIDTH,
            height = config.BUTTON_HEIGHT,
            x = config.START_X_BUTTON_RESET,
            y = config.START_Y_BUTTON_RESET
        )

        self.treeViewCanvasKanan = ttk.Treeview(
            self.canvasBlockRight,
            columns = ("Barang", "Jumlah", "Harga", "Subtotal"),
            show = "headings" 
        )

        self.treeViewCanvasKanan.heading(
            "Barang",
            text = "Barang"
        )

        self.treeViewCanvasKanan.heading(
            "Jumlah",
            text = "Jumlah"
        )

        self.treeViewCanvasKanan.heading(
            "Harga",
            text = "Harga"
        )

        self.treeViewCanvasKanan.heading(
            "Subtotal",
            text = "Subtotal"
        )

        self.treeViewCanvasKanan.column(
            "Barang", 
            width = 150
        )

        self.treeViewCanvasKanan.column(
            "Jumlah", 
            width = 50,
            anchor = "center"
        )

        self.treeViewCanvasKanan.column(
            "Harga", 
            width = 80,
            anchor = "center"
        )

        self.treeViewCanvasKanan.column(
            "Subtotal", 
            width = 90,
            anchor = "center"
        )

        self.treeViewCanvasKanan.place(
            width = config.FRAME_CANVAS_KANAN_WIDTH,
            x = config.START_X_FRAME_CANVAS_KANAN,
            y = config.START_Y_FRAME_CANVAS_KANAN,
            height = config.FRAME_CANVAS_KANAN_HEIGHT
        )

        self.labelImg = tk.Label(
            self.canvasBlockTop,
            image = self.tlogo,
            background = self.canvasBlockTop.cget("bg")
        )
        self.labelImg.place(
            x = config.START_X_LOGO,
            y = config.START_Y_LOGO
        )

        self.labelTotal = tk.Label(
            self.canvasBlockRight,
            font = (config.FONT_TYPE, config.FONT_SIZE),
            text = "Total : Rp0",
            background = self.canvasBlockRight.cget("bg"),
            foreground = config.WHITE
        )
        self.labelTotal.place(
            x = config.START_X_LABEL_TOTAL,
            y = config.START_Y_LABEL_TOTAL
        )

        self.labelNamaBarang = tk.Label(
            self.canvasBlockLeft,
            font = (config.FONT_TYPE, config.FONT_SIZE),
            text = config.NAMA_BARANG_MSG,
            background = self.canvasBlockLeft.cget("bg"),
            foreground = config.BLACK
        )
        self.labelNamaBarang.place(
            x = config.START_X_NAMA_BARANG, 
            y = config.START_Y_NAMA_BARANG
        )

        self.labelInputJumlah = tk.Label(
            self.canvasBlockLeft, 
            font = (config.FONT_TYPE, config.FONT_SIZE), 
            text = config.JUMLAH_BARANG_MSG, background = self.canvasBlockLeft.cget("bg"),
            foreground = config.BLACK
        )
        self.labelInputJumlah.place(
            x = config.START_X_INPUT_JUMLAH,
            y = config.START_Y_INPUT_JUMLAH)

        self.labelFooterTanggal = tk.Label(
            self.footerCanvas,
            font = (config.FONT_TYPE, config.FONT_SIZE),
            text = "Tanggal : 00/00/0000",
            background = self.footerCanvas.cget("bg"),
            foreground = config.BLACK)
        self.labelFooterTanggal.place(
            x = config.START_X_LABEL_TANGGAL,
            y = config.START_Y_LABEL_TANGGAL
        )