from KasirGuiWindow import KasirGuiWindow
from KasirGuiLogic import KasirGuiLogic
from KasirGuiData import KasirGuiData

if __name__ == "__main__":
    # 1. Menginisialisasi pembuatan objek jendela visual utama kelompok
    mainWindow = KasirGuiWindow()
    mainWindow.window_initializer()
      
    # 2. Mengeluarkan susunan canvases dan melahirkan seluruh objek widget komponen di layar
    mainWindow.draw_canvas()
    mainWindow.draw_widget()

    # 3. Menghubungkan kelas logika pengontrol aksi ke dalam objek jendela utama
    mainWindow.logic = KasirGuiLogic(mainWindow)

    # 4. MENGHUBUNGKAN PAKSA TOMBOL VISUAL KE KELAS LOGIKA DI SINI SETELAH widget SELESAI DIGAMBAR
    mainWindow.buttonTambahLeft.config(command=mainWindow.logic.tambah_barang)
    mainWindow.buttonHapusRight.config(command=mainWindow.logic.fungsi_hapus)
    mainWindow.buttonPembayaranRight.config(command=mainWindow.logic.fungsi_pembayaran)
    mainWindow.buttonKeluarTop.config(command = mainWindow.logic.keluar_app)
    mainWindow.buttonResetRight.config(command = mainWindow.logic.reset_pesanan)

    # 5. Menjalankan jam waktu sistem real-time dan menjaga tampilan kasir agar tetap menyala
    mainWindow.logic.footer_data()
    mainWindow.mainloop()