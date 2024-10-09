# Aplikasi Perbankan Sederhana

Aplikasi perbankan sederhana yang dibangun dengan Flask, dirancang untuk mengelola input saldo dan transaksi.

## Fitur

- Input saldo dari sumber offline.
- Antarmuka pengguna yang ramah untuk manajemen transaksi.
- Desain responsif untuk berbagai perangkat.

## Teknologi yang Digunakan

- Flask: Framework aplikasi web WSGI ringan di Python.
- HTML/CSS: Untuk antarmuka pengguna bagian depan.

## Instalasi

1. **Kloning repositori**:

   ```bash
   git clone https://github.com/iyungrozy/ebank.git
   cd ebank
   ```

2. **Instal paket yang diperlukan**:

   ```bash
   pip install -r requirements.txt
   ```

## Mengganti Database

Jika Anda ingin menggunakan database yang berbeda, ikuti langkah-langkah berikut:

1. **Buka file konfigurasi** di mana Anda mengatur URI database. Umumnya, ini ada di file `app.py`

2. **Temukan baris berikut**:

   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ebanking:hexagon123@panel.honjo.web.id:3306/ebanking'
   ```

3. **Ganti URI database** sesuai dengan detail database baru Anda port mysql akan selalu 3306. Format umumnya adalah:

   ```
   'mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>'
   ```

   Misalnya, jika Anda ingin menggunakan database lokal dengan username `user`, password `password`, dan nama database `mydatabase`, Anda akan menggantinya menjadi:

   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost:3306/mydatabase'
   ```

4. **Simpan perubahan** dan tutup file.

## Menjalankan Aplikasi

Untuk menjalankan aplikasi, jalankan perintah berikut:

```bash
python app.py
```

Buka browser Anda dan pergi ke `http://127.0.0.1:5001` untuk mengakses aplikasi.

## Penggunaan

- Gunakan aplikasi untuk menginput saldo dan mengelola transaksi.
- Ikuti petunjuk di antarmuka pengguna untuk menginput data.

## Kontribusi

Kontribusi sangat diterima! Silakan buat pull request atau buka masalah untuk perubahan atau perbaikan yang ingin Anda usulkan.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail.
```
