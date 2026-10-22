# Dokumentasi Proyek Ruang Usaha

> Panduan utama untuk melanjutkan pengembangan aplikasi Ruang Usaha. Perbarui dokumen ini setiap kali ada perubahan fitur, struktur, atau proses build.

## 1. Tautan penting

- **Repositori sumber:** https://github.com/poetate12-debug/Management-keuangan-usaha
- **Unduh APK langsung terbaru:** https://github.com/poetate12-debug/Management-keuangan-usaha/releases/download/latest/app-debug.apk
- **Daftar rilis:** https://github.com/poetate12-debug/Management-keuangan-usaha/releases/tag/latest
- **Build APK terbaru yang berhasil:** https://github.com/poetate12-debug/Management-keuangan-usaha/actions/runs/39661361566
- **Unduh paket APK (ZIP artifact):** https://api.github.com/repos/poetate12-debug/Management-keuangan-usaha/actions/artifacts/12372784335/zip
- **Commit build terakhir yang diketahui berhasil:** `4acc6bffd530734c029730686f41a403154fec49`

## 2. Cara mengunduh dan memasang APK

APK diterbitkan sebagai aset GitHub Release publik sehingga dapat diunduh sebagai file APK secara langsung.

1. Buka [tautan unduh APK langsung](https://github.com/poetate12-debug/Management-keuangan-usaha/releases/download/latest/app-debug.apk).
2. Tunggu hingga unduhan selesai.
3. Ketuk file `app-debug.apk` untuk memasang.
4. Jika Android meminta izin, izinkan instalasi dari sumber tersebut hanya untuk aplikasi yang digunakan.
5. Buka aplikasi dan uji fitur sebelum memasukkan banyak data.

Jika tautan gagal atau rilis belum selesai diperbarui, periksa [tab Actions](https://github.com/poetate12-debug/Management-keuangan-usaha/actions) dan [halaman rilis](https://github.com/poetate12-debug/Management-keuangan-usaha/releases/tag/latest).

## 3. Gambaran aplikasi

Ruang Usaha adalah aplikasi pencatatan keuangan usaha dengan antarmuka web yang dibungkus dalam aplikasi Android/WebView.

Fitur yang direncanakan/ditambahkan pada versi terbaru:
- Dashboard saldo total, pemasukan bulanan, pengeluaran bulanan, dan arus kas bersih.
- Pemilihan usaha/bisnis terlebih dahulu sebelum formulir transaksi.
- Katalog produk per usaha dengan nama, harga, dan satuan.
- Rincian beberapa produk dalam satu transaksi pemasukan, termasuk kuantitas dan harga; total dihitung dari baris produk.
- Penambahan dan pengeditan kategori.
- Dukungan beberapa akun/dompet.
- Tampilan modal dan formulir yang disesuaikan untuk layar ponsel.

**Penting:** keberhasilan build hanya memastikan proses kompilasi/pembuatan APK selesai; seluruh alur harus diuji langsung di perangkat. Pencatatan produk bukan berarti aplikasi sudah memiliki inventaris penuh. Jangan menganggap stok otomatis berkurang atau harga pokok/laba dihitung kecuali fitur tersebut telah ditambahkan dan diuji.

## 4. Penyimpanan data dan backup

Aplikasi menyimpan data transaksi dan pengaturan secara lokal pada WebView (localStorage) dalam ruang privat aplikasi. Pembaruan aplikasi yang mempertahankan ID paket Android dan identitas penandatanganan yang sama biasanya tidak menghapus data lokal. Data tidak otomatis tersinkron ke cloud atau perangkat lain.

- Jangan mencopot aplikasi atau menekan Hapus data jika ingin mempertahankan data lokal.
- Buat cadangan melalui **Pengaturan** sebelum pembaruan besar atau pemindahan perangkat.
- **Ekspor Data** membuat file JSON berisi usaha, akun, kategori, produk, dan transaksi.
- **Impor Data** membaca file JSON cadangan dan mengganti data yang sedang ada; selalu ekspor data saat ini terlebih dahulu.
- **Ekspor Excel** tersedia dari Pengaturan dan menghasilkan file `.xls` yang dapat dibuka di Excel/WPS, dengan lembar Transaksi, Usaha, Akun, Kategori, Produk, dan HPP. Cadangan JSON tetap terpisah untuk memulihkan seluruh data.
- Simpan file cadangan di folder Download atau lokasi aman lain. Uji impor menggunakan salinan cadangan sebelum mengandalkannya.
- Tidak ada sinkronisasi cloud otomatis.

## 5. Area sumber dan build

Alur build proyek sebelumnya menggunakan:
- `RuangUsahaAndroid/app/src/main/assets/index.html` — antarmuka web yang dibundel ke aplikasi Android.
- `patch_mobile.py` — skrip patch untuk penyesuaian tampilan/paket mobile.
- `patch_features.py` — skrip patch untuk perubahan fitur antarmuka.

Workflow GitHub Actions menyiapkan proyek, menjalankan skrip patch, membangun APK debug, lalu mengunggah artifact `RuangUsaha-debug-apk`.

Lakukan perubahan pada sumber atau skrip patch di repositori, kemudian build ulang. Jangan hanya mengedit APK hasil build karena perubahan tersebut tidak akan menjadi bagian dari sumber proyek.

## 6. Membuat APK baru

1. Buka repositori lalu pilih tab **Actions**.
2. Pilih workflow Android build.
3. Tekan **Run workflow** bila tersedia, atau lakukan commit ke branch yang dipantau workflow.
4. Tunggu sampai run berstatus **Success**.
5. Buka run tersebut dan unduh artifact `RuangUsaha-debug-apk`.
6. Ekstrak ZIP dan pasang `app-debug.apk` di perangkat uji.
7. Catat commit SHA, tanggal build, fitur yang berubah, dan hasil pengujian.

## 7. Checklist pengujian setiap build

- [ ] Aplikasi terbuka tanpa crash atau layar kosong.
- [ ] Tombol Catat berada di tengah navigasi bawah, lebih besar dan berwarna biru.
- [ ] Form transaksi tampil sebagai pop-up di atas navigasi; dropdown usaha, serta tombol Simpan dan Batal tidak tertutup navigasi.
- [ ] Saat pop-up terbuka, layar di belakangnya tidak ikut scroll.
- [ ] Tombol Catat transaksi dan Ekspor Excel tidak tampil di toolbar halaman; Ekspor Excel tersedia dari Pengaturan.
- [ ] Pengaturan dapat mengekspor dan mengimpor cadangan JSON.
- [ ] Dapat menambah dan memilih usaha.
- [ ] Dapat menambah/mengedit produk per usaha.
- [ ] Pemasukan dengan satu produk tersimpan dengan benar.
- [ ] Pemasukan dengan beberapa produk dan kuantitas menghitung total dengan benar.
- [ ] Pengeluaran mengubah ringkasan dashboard secara benar.
- [ ] Kategori dapat ditambah/diedit dan transaksi lama tetap benar.
- [ ] Beberapa akun/dompet dapat dipilih dan transaksi tercatat pada akun yang sesuai.
- [ ] Data tetap ada setelah aplikasi ditutup dan dibuka kembali.
- [ ] Backup dan pemulihan diuji jika fitur tersedia.
- [ ] Tombol dan modal tidak terpotong di layar ponsel.

## 8. Pemecahan masalah

**Artifact tidak terlihat**
- Pastikan membuka run yang benar, lalu gulir ke bagian Artifacts.
- Periksa apakah artifact sudah kedaluwarsa. Jika iya, jalankan build baru.

**Tidak bisa memasang ZIP**
- Ekstrak ZIP terlebih dahulu; Android memasang file APK, bukan ZIP.

**Android memblokir instalasi**
- Periksa izin instalasi aplikasi tidak dikenal untuk aplikasi pengelola file yang digunakan. Izinkan hanya jika sumber file dipercaya.

**Build gagal**
- Buka tab Actions, pilih run gagal, lalu baca log langkah berwarna merah. Perbaiki error pada sumber/skrip, commit, dan jalankan kembali.

**Data hilang**
- Penyimpanan lokal dapat hilang saat data aplikasi dibersihkan atau aplikasi dicopot. Pulihkan dari cadangan yang sudah dibuat dan diuji.

**Fitur tidak bekerja meski build berhasil**
- Catat langkah untuk mengulang masalah, perangkat/versi Android, dan screenshot. Perbaiki sumber, buat build baru, lalu ulangi checklist pengujian.

## 9. Pengembangan yang disarankan

1. Pastikan ekspor/impor backup mudah ditemukan dan pemulihannya teruji.
2. Tambahkan pengujian otomatis untuk perhitungan transaksi dan penyimpanan.
3. Siapkan build rilis dengan versioning dan penandatanganan yang dikelola dengan aman sebelum distribusi luas.
4. Jika perlu data lintas perangkat, rancang autentikasi, sinkronisasi cloud, privasi, dan backup.
5. Jika perlu inventaris, buat modul khusus untuk stok awal, barang masuk/keluar, penyesuaian stok, dan riwayat.
6. Pelihara catatan perubahan setiap versi.

## 10. Catatan versi

Pembaruan UI terakhir: formulir transaksi dioptimalkan sebagai panel/modal di atas navigasi dengan kontrol scroll internal; tombol Simpan/Batal diberi lapisan di atas navigasi; aksi Catat transaksi di toolbar dihapus; Ekspor Excel dipindah ke Pengaturan; impor/ekspor cadangan JSON tersedia di Pengaturan.

Isi bagian ini setiap kali ada pembaruan:

- **Tanggal:**
- **Versi:**
- **Commit SHA:**
- **Perubahan:**
- **Hasil pengujian:**
- **Masalah yang diketahui:**
- **Lokasi backup:**

---
Dokumen ini mencatat kondisi build yang diketahui pada 22 Oktober 2026. Periksa status Actions terbaru sebelum menganggap build tersebut sebagai versi paling baru.


## 11. Alur aplikasi terbaru: usaha, kategori, produk, dan HPP

**Catat transaksi**
1. Tekan tombol Catat.
2. Pilih jenis transaksi: Pemasukan, Pengeluaran, atau Transfer antar dompet.
3. Untuk pemasukan/pengeluaran, pilih usaha dari kartu bergambar dua kolom.
4. Formulir menampilkan kartu usaha terpilih di bagian atas dan kartu jenis transaksi berwarna hijau (pemasukan) atau merah (pengeluaran). Jenis dan usaha dipilih dari alur awal; ubah pilihan dengan menutup formulir dan memulai pencatatan kembali.
5. Untuk transfer, pilih dompet asal dan dompet tujuan; transfer tidak terikat ke usaha.

**Detail usaha**
- Buka tab Usaha dan ketuk Detail pada usaha untuk membuka halaman khusus usaha.
- Halaman detail menampilkan ringkasan statistik dan transaksi terbaru.
- Pilih Kategori usaha atau Produk usaha untuk membuka halaman khusus masing-masing. Data kategori dan produk ditampilkan menurut usaha terpilih.
- Kembali ke detail usaha untuk membuka menu Perhitungan HPP.

**Perhitungan HPP**
- HPP (Harga Pokok Produksi) dihitung dengan rumus: (total bahan baku + total tenaga kerja + overhead produksi) ÷ jumlah unit yang dihasilkan.
- Isi nama produk, jumlah unit, biaya bahan baku, biaya tenaga kerja, dan overhead.
- Hasil total biaya dan HPP per unit dihitung otomatis. Tekan Simpan perhitungan untuk mencatat hasil dalam riwayat HPP usaha tersebut.
- Perhitungan HPP adalah modul biaya sederhana. Angka tidak otomatis mengubah harga produk, stok persediaan, atau transaksi penjualan.

**Perlindungan data**
- Data HPP disimpan bersama data aplikasi. Ekspor cadangan JSON dari Pengaturan secara berkala, terutama sebelum update APK.
- Memperbarui aplikasi dengan paket/tanda tangan yang sama biasanya mempertahankan data lokal. Menghapus aplikasi, menghapus data aplikasi, atau reset perangkat dapat menghapus data.
- Setelah setiap build baru, uji satu transaksi pemasukan, satu pengeluaran, satu transfer, pengeditan kategori per usaha, produk pada dua usaha berbeda, dan satu kalkulasi HPP.

## 12. Foto usaha, navigasi kembali, dan HPP berbahan baku

### Foto usaha
- Pada tab Usaha, kartu memiliki area foto/ikon dan tombol kamera untuk memilih foto dari perangkat.
- Foto dikecilkan sebelum disimpan ke data lokal usaha, lalu ditampilkan pada kartu daftar usaha dan kartu usaha di dashboard.
- Foto dapat diubah dengan memilih gambar baru dari tombol kamera di kartu. Foto yang terlalu besar tetap akan dikompresi agar tidak terlalu cepat memenuhi penyimpanan lokal.

### Kartu usaha di dashboard
- Kartu ringkasan per usaha menampilkan logo/ikon atau foto, nama usaha, pemasukan, pengeluaran, dan arus kas bersih.
- Tombol aksi cepat pemasukan, pengeluaran, dan detail pada kartu dashboard dihilangkan. Ketuk kartu untuk membuka detail usaha.

### Tombol kembali dan Batal
- Tombol kembali pada halaman kategori, produk, HPP, dan detail usaha disambungkan ke alur navigasi aplikasi.
- Tombol Batal/Tutup pada pop-up menutup pop-up yang sedang aktif.
- Tombol Back bawaan Android menggunakan riwayat aplikasi: pop-up ditutup terlebih dahulu, lalu kembali dari halaman kategori/produk/HPP ke detail usaha, dari detail usaha ke daftar usaha, dan dari tab ke halaman sebelumnya. Jika tidak ada halaman sebelumnya, kembali ke Beranda.

### HPP dengan rincian bahan baku
- Masukkan nama produk yang dibuat dan jumlah unit hasil produksi.
- Tambahkan beberapa baris bahan baku, misalnya kertas foto, tinta, laminasi, lem, atau komponen lain. Setiap baris berisi nama bahan, jumlah pemakaian, dan harga per unit.
- Total biaya bahan baku dihitung sebagai jumlah dari kuantitas × harga per unit untuk tiap bahan.
- Total biaya produksi = total bahan baku + tenaga kerja + overhead.
- HPP per unit = total biaya produksi ÷ jumlah unit hasil produksi.
- Riwayat HPP menyimpan rincian bahan, biaya, jumlah unit, dan HPP per unit per usaha.
- HPP merupakan kalkulator pencatatan biaya. Ia belum secara otomatis membuat transaksi, menurunkan stok, atau mengubah harga jual produk.

**Checklist pengujian tambahan setelah update:** unggah foto pada satu usaha dan periksa tampil di dashboard; ketuk kartu dashboard untuk membuka detail; buka kategori lalu tekan kembali bawaan Android; buka HPP, tambahkan setidaknya dua bahan baku, simpan, lalu periksa riwayat.
