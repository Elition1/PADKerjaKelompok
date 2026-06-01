from tkinter import messagebox
import ConfigGUI as config
import time

class KasirGuiLogic:
    def __init__(self, windowKasir):
        self.windowKasir = windowKasir

        # List untuk mengambil barang
        self.pesananUser = None

    def non_background_effects(self, event = None):
        self.windowKasir.comboBoxCanvasLeft.selection_clear()

    def tambah_barang(self):
        try:
            jumlahBarang = int(self.windowKasir.jumlahBarangVar.get())
            print(jumlahBarang)
            print("Button Clicked")
        except ValueError:
            messagebox.showerror(title="Error", message=config.ERROR_MSG_PENAMBAHAN)
            self.windowKasir.jumlahBarangEntryBoxCanvasLeft.delete(0, 'end')

    def keluar_app(self):
        konfirmasi = messagebox.askyesno(title = "Keluar", message = config.EXIT_MSG)
        if konfirmasi:
            messagebox.showinfo(title = "YAH", message = config.CONFIRM_MSG)
            time.sleep(config.SLEEP_DURATION)
            self.windowKasir.destroy()     
            
    def footer_data(self):
        tanggalSekarang = time.strftime("Tanggal : %d/%m/%Y")
        waktuSekarang = time.strftime("Pukul : %H:%M")

        self.windowKasir.labelFooterTanggal.config(text = tanggalSekarang)
        # self.windowKasir.labelFooterWaktu.config(text = waktuSekarang)

        self.windowKasir.after(1000, self.footer_data)