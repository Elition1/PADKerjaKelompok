import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import ConfigGUI as config

# Menghubungkan kelas data pandas tugasmu ke dalam file logika
from KasirGuiData import KasirGuiData

class KasirGuiLogic:
    def __init__(self, windowKasir):
        self.windowKasir = windowKasir
        # Dictionary menampung data pesanan sementara sebelum dibayar
        self.pesananUser = {}
        # Menyiapkan objek simpan data pandas untuk laporan CSV tugasmu
        self.laporan_data = KasirGuiData()

    def non_background_effects(self, event = None):
        self.windowKasir.comboBoxCanvasLeft.selection_clear()

    # method untuk menambah produk ke listbox menggunakan tombol tambah
    def tambah_barang(self):
        try:
            jumlahBarang = int(self.windowKasir.jumlahBarangVar.get())
            produk_terpilih = self.windowKasir.comboBoxCanvasLeft.get()

            if not produk_terpilih:
                messagebox.showwarning("Peringatan", "Pilih produk terlebih dahulu!")
                return
            if jumlahBarang <= 0:
                messagebox.showwarning("Peringatan", "Jumlah barang harus lebih dari 0!")
                return

            # Menyimpan data produk ke dictionary pesananUser agar bisa dibaca pandas
            self.pesananUser[produk_terpilih] = {
                "Harga": 50000, # dumi harga default produk kelompok Rp50.000
                "jumlahBarang": jumlahBarang
            }

            # menampilkan barang produk yang dipilih ke listbox milik temanmu
            self.windowKasir.frameCanvasKanan.insert("end", f"{produk_terpilih} x{jumlahBarang}")
            print(jumlahBarang)
            print("Button Clicked")
        except ValueError:
            messagebox.showerror(title="Error", message=config.ERROR_MSG_PENAMBAHAN)
            self.windowKasir.jumlahBarangEntryBoxCanvasLeft.delete(0, 'end')

    # method untuk menghapus item yang sedang diklik/dipilih di Listbox temanmu
    def fungsi_hapus(self):
        seleksi = self.windowKasir.frameCanvasKanan.curselection()
        if seleksi:
            item_teks = self.windowKasir.frameCanvasKanan.get(seleksi)
            nama_produk = item_teks.split(" x")[0] 
            
            if nama_produk in self.pesananUser:
                del self.pesananUser[nama_produk]
                
            self.windowKasir.frameCanvasKanan.delete(seleksi)
            messagebox.showinfo("Sukses", f"{nama_produk} dihapus dari daftar")
        else:
            messagebox.showwarning("Error", config.ERROR_MSG_PENGHAPUSAN)

    # KODE BARU: Kebal dari jebakan ValueError palsu
    def fungsi_pembayaran(self):
        # 1. Cek apakah ada barang yang dibeli
        if not self.pesananUser:
            messagebox.showwarning("Peringatan", "Pesanan masih kosong!")
            return
            
        # 2. Hitung total belanjaan secara aman dengan pembulatan bulat
        total = 0
        for nama, data in self.pesananUser.items():
            harga = int(data.get("Harga", 50000))
            jumlah = int(data.get("jumlahBarang", 1))
            total += (harga * jumlah)
        
        # 3. Munculkan dialog box kecil untuk input uang belanjaan
        from tkinter import simpledialog
        bayar_input = simpledialog.askstring("Pembayaran", f"Total Harga : Rp{total:,}\nMasukkan Uang Pembayaran:")
        
        # Jika user menekan cancel atau mengosongkan input, keluar dengan damai
        if bayar_input is None or bayar_input.strip() == "":
            return

        # 4. Bersihkan input otomatis dari titik/huruf, hanya sisakan angka murni
        bayar_clean = "".join(filter(str.isdigit, bayar_input))
        
        # Jika input ternyata isinya huruf semua/tidak ada angka sama sekali
        if not bayar_clean:
            messagebox.showerror("Error", "Masukkan nominal uang menggunakan angka saja!")
            return
            
        bayar = int(bayar_clean)
        
        # 5. Hitung diskon kelompok menggunakan pembagian bulat // agar tetap berupa INT murni
        diskon = 0
        if total > 100000:
            diskon = (total * 10) // 100
        elif total > 50000:
            diskon = (total * 5) // 100

        total_akhir = total - diskon
        
        # 6. Cek kecukupan uang
        if bayar < total_akhir:
            messagebox.showerror("Gagal", f"Uang kurang! Total harus dibayar: Rp{total_akhir:,}")
            return
            
        kembalian = bayar - total_akhir
        
        # 7. TUGAS PANDAS KAMU: MENCATAT TRANSAKSI KE FILE CSV
        try:
            self.laporan_data.simpan_transaksi(self.pesananUser)
        except Exception as e:
            print(f"Gagal mencatat CSV tapi pembayaran tetap lanjut: {e}")
            
        # 8. Cetak nota struk belanjaan asli kamu ke pop-up layar
        isi_struk = self.cetakStruk(total, diskon, bayar, kembalian)
        messagebox.showinfo("Pembayaran Berhasil", isi_struk)
        
        # 9. Bersihkan pesanan setelah sukses dibayar
        self.pesananUser.clear()
        self.windowKasir.frameCanvasKanan.delete(0, tk.END)
        self.windowKasir.jumlahBarangEntryBoxCanvasLeft.delete(0, tk.END)

    def cetakStruk(self, total, diskon, bayar, kembalian):
        sekarang = str(datetime.now()) 
        lines = []
        lines.append("--------------------------------------------------")
        lines.append(f"Waktu sekarang: {sekarang[:19]}")
        lines.append("--------------------------------------------------")
        lines.append("Daftar Pesanan:")
        for i, (nama, data) in enumerate(self.pesananUser.items()):
            subTotal = data["jumlahBarang"] * data["Harga"]
            lines.append(f"{i+1}. {nama} | Rp{subTotal:,}")
        lines.append("--------------------------------------------------")
        lines.append(f"Total  : Rp{total:,}")
        lines.append(f"Diskon : Rp{diskon:,}")
        lines.append(f"Bayar : Rp{bayar:,}")
        lines.append(f"Kembalian : Rp{kembalian:,}")
        return "\n".join(lines)

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
        
        self.windowKasir.labelFooterWaktu = tk.Label(self.windowKasir.footerCanvas, font=(config.FONT_TYPE, config.FONT_SIZE), bg=config.WHITE, fg=config.BLACK)
        self.windowKasir.labelFooterWaktu.place(x=config.START_X_LABEL_WAKTU, y=config.START_Y_LABEL_TANGGAL)
        self.windowKasir.labelFooterWaktu.config(text = waktuSekarang)

        self.windowKasir.after(1000, self.footer_data)