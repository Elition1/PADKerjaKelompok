import pandas as pd
import os

class KasirGuiData:
    def __init__(self):
        # MENGUNCI JALUR: Mengambil alamat folder tempat file ini berada secara otomatis
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Menggabungkan alamat folder dengan nama file CSV
        self.nama_file = os.path.join(base_dir, "COBA KONTOL.csv")
        
        # membuat daftar nama kolom untuk bagian judul tabel laporan penjualan
        self.kolom_header = ["No", "Nama Barang", "Harga Barang", "Jumlah Barang"]

    def simpan_transaksi(self, pesanan_user):
        data_tabel = []
        
        # 1. Mengambil nomor urut terakhir jika file csv sudah ada sebelumnya
        no = 1
        if os.path.exists(self.nama_file):
            df_lama = pd.read_csv(self.nama_file)
            no = len(df_lama) + 1 

        # 2. Bagian pengulangan untuk mengambil masing-masing data barang produk yang dibeli user
        for nama, data in pesanan_user.items():
            baris = {
                "No": no,
                "Nama Barang": nama,
                "Harga Barang": data["Harga"],
                "Jumlah Barang": data["jumlahBarang"]
            }
            data_tabel.append(baris)
            no += 1 

        # 3. Membuat DataFrame baru dari list data tabel yang sudah dikumpulkan
        df_baru = pd.DataFrame(data_tabel)

        # 4. Mencoba menyimpan hasil DataFrame ke dalam file laporan excel csv
        if os.path.exists(self.nama_file):
            df_baru.to_csv(self.nama_file, mode='a', header=False, index=False, encoding='utf-8')
        else:
            df_baru.to_csv(self.nama_file, mode='w', header=self.kolom_header, index=False, encoding='utf-8')