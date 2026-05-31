#import library buat pembuatan GUI
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

#membuat dictionary buat menyimpan pesanan user
pesananUser = {}

#method untuk mencetak struk untuk ditampilkan setelah pembayaran
def cetakStruk(total, diskon, bayar, kembalian):
    sekarang = str(datetime.now()) 
    lines = []
    lines.append("--------------------------------------------------")
    lines.append(f"Waktu sekarang: {sekarang[:19]}")
    lines.append("--------------------------------------------------")
    lines.append("Daftar Pesanan:")
    
    for i, x in enumerate(pesananUser):
        subTotal = pesananUser[x]["jumlahBarang"] * pesananUser[x]["Harga"]
        lines.append(f"{i+1}. {x} | Rp{subTotal}")
        
    lines.append("--------------------------------------------------")
    lines.append(f"Total  : Rp{total}")
    lines.append(f"Diskon : Rp{diskon}")
    lines.append(f"Bayar : Rp{bayar}")
    lines.append(f"Kembalian : Rp{kembalian}")
    
    hasil = "\n".join(lines)
    return hasil

# method untuk menampilkan ulang hasil tabel produk
def refresh_table():
    for item in tree.get_children():
        tree.delete(item)
    # bagian pengulangan untuk menampilkan barang produk setelah terjadi perubahan
    for nama, data in pesananUser.items():
        tree.insert(
            "",
            "end",
            values=(
                nama,
                f"Rp{data['Harga']}",
                data["jumlahBarang"]
            )
        )

# method untuk menambah produk ke tabel menggunakan tombol tambah
def fungsi_tambah():
    # mengambil data yang dapat dari entry box
    nama = entrynamabarang.get()
    harga = entryhargabarang.get()
    jumlah = entryjumlahbarang.get()

    # jika ketiga data tersebut diisi akan mencoba disimpan ke tabel
    if nama and harga and jumlah:
        try:
            pesananUser[nama] = {
                "Harga": int(harga),
                "jumlahBarang": int(jumlah)
            }
            total = sum(item["Harga"] * item["jumlahBarang"] for item in pesananUser.values())
            totallabellabel.config(text=f"Total Harga : Rp{total:,}")
            # mengulangi tabel setelah perubahan
            refresh_table()
            
            # menghapus data setelah penambahan  produk
            entrynamabarang.delete(0, tk.END)
            entryhargabarang.delete(0, tk.END)
            entryjumlahbarang.delete(0, tk.END)
        #jika data harga dan jumlah barang tidak berupa bilangan maka melempar sebuah error
        except ValueError:
            messagebox.showerror("Error", "Harga dan Jumlah harus angka!")
    # menyuruh user untuk mengisi data yang kosong
    else:
        messagebox.showwarning("Peringatan", "Isi semua data barang!")

# method untuk menghapus barang-barang yang ada di tabel produk
def fungsi_hapus():
    nama = entrynamabarang.get()
    if nama in pesananUser:
        del pesananUser[nama]
        total = sum(item["Harga"] * item["jumlahBarang"] for item in pesananUser.values())
        totallabellabel.config(text=f"Total Harga : Rp{total:,}")

        refresh_table()

        entrynamabarang.delete(0, tk.END)
        messagebox.showinfo("Sukses", f"{nama} dihapus dari daftar")
    else:
        messagebox.showwarning("Error", "Masukkan nama barang di kolom input untuk menghapus")

# method untuk tombol pembayaran dan mencoba untuk melihat apakah transaksimya berhasil
def fungsi_pembayaran():
    # mencoba pembayaran yang di input user dari entry pembayaran
    try:
        total = sum(item["Harga"] * item["jumlahBarang"] for item in pesananUser.values())
        if total == 0:
            messagebox.showwarning("Peringatan", "Pesanan masih kosong!")
            return
        # mengambil data pembayaran tersebut
        bayar_input = inputpembayaran.get()
        # jika pembayaran tersebut belum diisi maka dikasih error
        if not bayar_input:
            messagebox.showwarning("Peringatan", "Masukkan uang pembayaran!")
            return

        bayar = float(bayar_input)
        
        # mendapatkan diskon jika user membeli barang melewati harga total tertentu
        diskon = 0
        if total > 100000:
            diskon = total * 0.10
        elif total > 50000:
            diskon = total * 0.05

        # menghitung hasil akhir total harga barang    
        total_akhir = total - diskon
        
        # jika pembayaran tidak mencukupi maka kasih pesan
        if bayar < total_akhir:
            messagebox.showerror("Gagal", f"Uang kurang! Total harus dibayar: Rp{total:,}")
        else:
            # menghitung kembalian jika pembayaran melewati total harga yang dibeli
            kembalian = bayar - total_akhir
            
            # mengisi informasi pembayaran ke struk
            isi_struk = cetakStruk(total, diskon, bayar, kembalian)
            messagebox.showinfo("Pembayaran Berhasil", isi_struk)
            
            # menghapus pesanan user setelah pembayaran
            pesananUser.clear()

            # mengupdate tabel produk
            refresh_table()
            totallabellabel.config(text="Total Harga : Rp0")
            inputpembayaran.delete(0, tk.END)
    # jika input yang dikasih tidak merupakan bilangan menampilkan error
    except ValueError:
        messagebox.showerror("Error", "Masukkan nominal uang dengan benar!")

# inisialisasi GUI yaitu main dengan title, warna belakang dan ukuran window GUI
main = tk.Tk()
main.title("windowKasir")
main.config(bg="#e9caf2")
main.geometry("900x565")

# window GUI tidak bisa diubah ukurannya
main.resizable(False, False)

# penamaan entry box yang diperlukan yaitu nama, harga, dan jumlah barang serta pembayaran barang
entrynamabarang = tk.Entry(master=main)
entrynamabarang.config(bg="#fff", fg="#000", font=("TkFixedFont", 13))
entrynamabarang.place(x=150, y=26, width=200, height=30)

entryhargabarang = tk.Entry(master=main)
entryhargabarang.config(bg="#fff", fg="#000", font=("TkFixedFont", 13))
entryhargabarang.place(x=150, y=76, width=200, height=30)

entryjumlahbarang = tk.Entry(master=main)
entryjumlahbarang.config(bg="#fff", fg="#000", font=("TkFixedFont", 13))
entryjumlahbarang.place(x=150, y=126, width=200, height=30)

inputpembayaran = tk.Entry(master=main)
inputpembayaran.config(bg="#fff", fg="#000", font=("TkFixedFont", 13))
inputpembayaran.place(x=150, y=226, width=200, height=30)

# dikasih label untuk mengetahui masing-masing entry box
tk.Label(master=main, text="Nama Barang :", bg="#e9caf2", font=("TkFixedFont", 13)).place(x=30, y=18, height=40)
tk.Label(master=main, text="Harga Barang :", bg="#e9caf2", font=("TkFixedFont", 13)).place(x=30, y=69, height=40)
tk.Label(master=main, text="Jumlah Barang :", bg="#e9caf2", font=("TkFixedFont", 13)).place(x=16, y=116, height=40)
tk.Label(master=main, text="Pembayaran :", bg="#e9caf2", font=("TkFixedFont", 13)).place(x=35, y=221, height=40)

totallabellabel = tk.Label(master=main, text="Total Harga : Rp0")
totallabellabel.config(bg="#e9caf2", fg="#000", font=("TkFixedFont", 13, "bold"))
totallabellabel.place(x=438, y=169)

# menampilkan tabel daftar produk yang di inputkan
frameDaftar = tk.Frame(main, bg="#ffffff", bd=2, relief="solid")
frameDaftar.place(x=400, y=20, width=270, height=130)

# membuat label menunjukkan list box adalah daftar produk yang diinput
tk.Label(frameDaftar, text="Daftar Barang", bg="#ffffff", font=("TkFixedFont", 12, "bold")).pack()

# membuat 3 daftar dengan masing-maisng menampilkan kolom barang, harga, dan jumlah
tree = ttk.Treeview(frameDaftar, columns=("Barang", "Harga", "Jumlah"), show="headings", height=4)

tree.heading("Barang", text="Barang")
tree.heading("Harga", text="Harga")
tree.heading("Jumlah", text="Jumlah")

tree.column("Barang", width=90)
tree.column("Harga", width=90)
tree.column("Jumlah", width=70)

# menyusun masing kolom barang
tree.pack(fill="both", expand=True)

# membuat tombol-tombol yaitu penambahan, penghapusan, dan pembayaran masing-masing barang dengan fungsi method sendiri
buttontambah = tk.Button(master=main, text="Tambah", command=fungsi_tambah, bg="#41ef4f", font=("TkFixedFont", 
                                                                                                13, "bold"))
buttontambah.place(x=150, y=170, width=90, height=40)

buttonpembayaran = tk.Button(master=main, text="Pembayaran", command=fungsi_pembayaran, bg="#6c75ca", 
                             font=("TkFixedFont", 13, "bold"))
buttonpembayaran.place(x=150, y=277, width=200, height=40)

buttonhapus = tk.Button(master=main, text="Hapus", command=fungsi_hapus, bg="#cc4040", font=("TkFixedFont", 13, "bold"))
buttonhapus.place(x=260, y=170, width=90, height=40)

# menjalankan window dengan hasil program diatas dan menjaga tampilan tersebut menggunakan mainloop
main.mainloop()