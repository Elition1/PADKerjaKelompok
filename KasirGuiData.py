import pandas as pd
import os

class KasirGuiData:
    def __init__(self):
        # MENGUNCI JALUR: Mengambil alamat folder tempat file ini berada secara otomatis
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Menggabungkan alamat folder dengan nama file CSV
        self.nama_file = os.path.join(base_dir, "Laporan.csv")

        # membuat daftar nama kolom untuk bagian judul tabel laporan penjualan
        self.kolom_header = ["No", "Nama Barang", "Harga Barang", "Jumlah Barang", "SubTotal"]

    def simpan_transaksi(self, pesanan_user):
        data_tabel = []
        
        # 1. Mengambil nomor urut terakhir jika file csv sudah ada sebelumnya
        no = 1
        if os.path.exists(self.nama_file):
            df_lama = pd.read_csv(self.nama_file, sep = ';')
            no = len(df_lama) + 1

        # 2. Bagian pengulangan untuk mengambil masing-masing data barang produk yang dibeli user
        total = 0        
        for nama, data in pesanan_user.items():
            subtotal = data["Harga"] * data["jumlahBarang"] 
            total += subtotal
            baris = {
                "No": no,
                "Nama Barang": nama,
                "Harga Barang": data["Harga"],
                "Jumlah Barang": data["jumlahBarang"],
                "SubTotal": subtotal
            }
            data_tabel.append(baris)


        baris_total = {
            "No": "Total :",
            "Nama Barang" : "",
            "Harga Barang" : "",
            "Jumlah Barang" : "",
            "SubTotal" : total
        }
        data_tabel.append(baris_total)
        # 3. Membuat DataFrame baru dari list data tabel yang sudah dikumpulkan
        df_baru = pd.DataFrame(data_tabel, columns = self.kolom_header)
        
        # 4. Mencoba menyimpan hasil DataFrame ke dalam file laporan excel csv
        if os.path.exists(self.nama_file):
            df_baru.to_csv(self.nama_file, mode='a', header=False, index=False, sep = ';', lineterminator='\n', encoding='utf-8')
        else:
            df_baru.to_csv(self.nama_file, mode='w', header=self.kolom_header, index=False, sep = ';', lineterminator='\n', encoding='utf-8')