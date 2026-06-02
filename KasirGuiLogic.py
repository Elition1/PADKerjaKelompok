import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import csv
import ConfigGUI as config
import os

# Menghubungkan kelas data pandas tugasmu ke dalam file logika
from KasirGuiData import KasirGuiData

class KasirGuiLogic:
    def __init__(self, windowKasir):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.windowKasir = windowKasir
        # Dictionary menampung data pesanan sementara sebelum dibayar
        self.pesananUser = {}
        # Ambil Data CSV
        path_csv_produk = os.path.join(base_dir, "MenuProduk.csv")
        # Menyiapkan objek simpan data pandas untuk laporan CSV tugasmu
        self.laporan_data = KasirGuiData()
        self.ambil_data(path_csv_produk)

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

            nama_produk, harga_text = produk_terpilih.split(" - Rp")
            harga = int(harga_text.replace(",", ""))

            if produk_terpilih in self.pesananUser:
                messagebox.showerror(title="Error", message=config.ERROR_MSG_DUPLIKAT)
                self.pesananUser[produk_terpilih]["jumlahBarang"] = jumlahBarang

                semua_item = self.windowKasir.treeViewCanvasKanan.get_children()

                for data_item in semua_item:
                    hasil_item = self.windowKasir.treeViewCanvasKanan.item(data_item, "values")
                    if hasil_item and hasil_item[0] == nama_produk:
                        subtotal = jumlahBarang * harga 
                        self.windowKasir.treeViewCanvasKanan.item(
                            data_item,
                            values = (
                                nama_produk,
                                jumlahBarang,
                                f"Rp{harga:,}",
                                f"Rp{subtotal:,}"
                            )
                        )
            # Menyimpan data produk ke dictionary pesananUser agar bisa dibaca pandas
            else:    
                self.pesananUser[produk_terpilih] = {
                    "Harga": harga, # dumi harga default produk kelompok Rp50.000
                    "jumlahBarang": jumlahBarang
                }
                subtotal = harga * jumlahBarang
                # menampilkan barang produk yang dipilih ke listbox milik temanmu
                self.windowKasir.treeViewCanvasKanan.insert(
                    "", 
                    "end",
                    values = (
                        nama_produk,
                        jumlahBarang,
                        f"Rp{harga:,}",
                        f"Rp{subtotal:,}"
                    )
                )
                
            total = 0
            for data in self.pesananUser.values():
                total += data["Harga"] * data["jumlahBarang"]

            self.windowKasir.labelTotal.config(text = f"Total : Rp{total:,}")
        except ValueError:
            messagebox.showerror(title="Error", message=config.ERROR_MSG_PENAMBAHAN)
            self.windowKasir.jumlahBarangEntryBoxCanvasLeft.delete(0, 'end')

    # method untuk menghapus item yang sedang diklik/dipilih di Listbox temanmu
    def fungsi_hapus(self):
        seleksi = self.windowKasir.treeViewCanvasKanan.selection()
        if seleksi:
           item_id = seleksi[0]

           data_item = self.windowKasir.treeViewCanvasKanan.item(item_id)
           nama_produk = data_item["values"][0]

           for key in list(self.pesananUser.keys()):
               if key.startswith(nama_produk):
                   del self.pesananUser[key]
                   break

           self.windowKasir.treeViewCanvasKanan.delete(item_id)

           total = 0

           for data in self.pesananUser.values():
               total += data["Harga"] * data["jumlahBarang"]

           self.windowKasir.labelTotal.config(text = f"Total : Rp{total:,}")

           messagebox.showinfo(
              "Sukses",
              f"{nama_produk} dihapus dari daftar"
           )
        else:
           messagebox.showwarning(
               "Error",
               config.ERROR_MSG_PENGHAPUSAN
           )

    # KODE BARU: Kebal dari jebakan ValueError palsu
    def fungsi_pembayaran(self):
        # 1. Cek apakah ada barang yang dibeli
        if not self.pesananUser:
            messagebox.showwarning("Peringatan", config.ERROR_MSG_PEMBAYARAN_TIDAK_ADA_PESANAN)
            return
            
        # 2. Hitung total belanjaan secara aman dengan pembulatan bulat
        subtotal = 0
        for name, data in self.pesananUser.items():
            subtotal += int(data.get("Harga")) * int(data.get("jumlahBarang"))
        total = subtotal
        
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
            messagebox.showerror(
                "Gagal",
                config.ERROR_MSG_PEMBAYARAN_TIDAK_MENCUKUPI.format(total_akhir = total_akhir)
            )
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
        self.reset_pesanan()

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

    def ambil_data(self, path_csv_produk):
        listProduk = []

        with open(path_csv_produk, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                listProduk.append(f"{row['Nama']} - Rp{row['Harga']}")

        self.windowKasir.comboBoxCanvasLeft['values'] = listProduk

    def reset_pesanan(self):
        self.pesananUser.clear()

        for item in self.windowKasir.treeViewCanvasKanan.get_children():
           self.windowKasir.treeViewCanvasKanan.delete(item)

        total = 0

        for data in self.pesananUser.values():
               total += data["Harga"] * data["jumlahBarang"]

        self.windowKasir.labelTotal.config(text = f"Total : Rp{total:,}")


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