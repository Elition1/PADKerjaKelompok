from KasirGuiWindow import KasirGuiWindow
from KasirGuiLogic import KasirGuiLogic

# inisialisasi blok utama untuk mengeksekusi program jalannya window GUI kasir
if __name__ == "__main__":
    # 1. Inisialisasi pembuatan jendela tampilan aplikasi utama dari file window kasir
    mainWindow = KasirGuiWindow()
    mainWindow.window_initializer()
    
    # 2. Menghubungkan kelas logika untuk mengontrol aksi tombol ke dalam objek jendela utama
    mainWindow.logic = KasirGuiLogic(mainWindow)
    
    # 3. KELUARKAN ATAU GAMBAR SEMUA KANVAS DAN WIDGET TERLEBIH DAHULU
    mainWindow.draw_canvas()
    mainWindow.draw_widget()
    
    # 4. SETELAH WIDGET DIGAMBAR, BARU HUBUNGKAN TOMBOL VISUAL KE KELAS LOGIKA
    mainWindow.buttonTambahLeft.config(command=mainWindow.logic.tambah_barang)
    mainWindow.buttonHapusRight.config(command=mainWindow.logic.fungsi_hapus)
    mainWindow.buttonPembayaranRight.config(command=mainWindow.logic.fungsi_pembayaran)
    
    # 5. Menjalankan jam waktu sistem dan menjaga tampilan tetap menyala menggunakan mainloop
    mainWindow.logic.footer_data()
    mainWindow.mainloop()