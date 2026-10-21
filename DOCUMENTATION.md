# Dokumentasi Proyek Ruang Usaha

> Panduan utama untuk melanjutkan pengembangan aplikasi Ruang Usaha. Perbarui dokumen ini setiap kali ada perubahan fitur, struktur, atau proses build.

## 1. Tautan penting

- **Repositori sumber:** https://github.com/poetate12-debug/Management-keuangan-usaha
- **Build APK terbaru yang berhasil:** https://github.com/poetate12-debug/Management-keuangan-usaha/actions/runs/39661361566
- **Unduh paket APK (ZIP artifact):** https://api.github.com/repos/poetate12-debug/Management-keuangan-usaha/actions/artifacts/12372784335/zip
- **Commit build terakhir yang diketahui berhasil:** `4acc6bffd530734c029730686f41a403154fec49`

## 2. Cara mengunduh dan memasang APK

Saat dokumentasi ini ditulis, hasil build disimpan sebagai artifact GitHub Actions bernama `RuangUsaha-debug-apk`. GitHub menyediakan artifact ini sebagai ZIP, bukan tautan langsung ke file APK di dalam ZIP.

1. Buka halaman [build terbaru](https://github.com/poetate12-debug/Management-keuangan-usaha/actions/runs/39661361566).
2. Gulir ke bagian **Artifacts**.
3. Unduh **RuangUsaha-debug-apk**.
4. Ekstrak ZIP menggunakan aplikasi File di Android.
5. Ketuk `app-debug.apk` untuk memasang.
6. Jika diminta, izinkan instalasi dari sumber tersebut hanya untuk aplikasi pengelola file yang digunakan.
7. Jalankan pengujian sebelum memasukkan data usaha sungguhan.

Artifact terakhir tercatat kedaluwarsa pada **19 Januari 2027**. Jika tautan artifact sudah tidak tersedia, jalankan workflow build kembali dari tab Actions.

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

Aplikasi menggunakan penyimpanan lokal WebView/browser (localStorage) untuk data antarmuka. Data tidak otomatis tersinkron ke cloud atau perangkat lain.

- Membersihkan data aplikasi, mencopot aplikasi, atau tindakan tertentu pada penyimpanan dapat menghapus data lokal.
- Sebelum memperbarui atau memasang ulang aplikasi, buat cadangan menggunakan fitur ekspor/backup yang tersedia jika ada.
- Uji proses pemulihan backup dengan data percobaan.
- Jangan mengandalkan sinkronisasi cloud kecuali fitur tersebut memang sudah dibuat.

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
