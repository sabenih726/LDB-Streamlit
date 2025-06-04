# 📑 Ekstraksi Dokumen Imigrasi

Aplikasi berbasis Streamlit untuk mengekstrak data dari dokumen PDF imigrasi seperti SKTT, EVLN, ITAS, ITK, dan Notifikasi. Aplikasi ini dilengkapi dengan fitur login, pengolahan file, rename otomatis, dan export ke Excel/ZIP.

## 🚀 Cara Menjalankan Aplikasi

1. Pastikan Python 3.8+ telah terpasang
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:

```bash
streamlit run app.py
```

## 🗂️ Struktur Proyek

```
app/
├── app.py              # Entry point utama aplikasi
├── auth.py             # Fungsi autentikasi (login, logout, hash password)
├── extractors.py       # Fungsi ekstraksi untuk SKTT, EVLN, ITAS, ITK, Notifikasi
├── file_handler.py     # Pemrosesan file PDF, rename file, zip file, export Excel
├── helpers.py          # Fungsi bantu (clean text, format tanggal, buat nama file)
├── ui_components.py    # UI halaman login, sidebar, upload, dan tampilan hasil
```

## 🔐 Login Pengguna

Akun login saat ini disimpan secara lokal:

* **sinta / sinta123**
* **ainun / ainun123**
* **fatih / fatih123**

> *Untuk keamanan produksi, gunakan sistem autentikasi berbasis database atau file terenkripsi.*

## 📌 Catatan Tambahan

* File yang diproses akan disimpan sementara dalam direktori sementara (`tempfile`) dan dihapus setelah selesai.
* Nama file baru dibentuk dari `Nama` dan `Nomor Paspor` (jika tersedia).
* Output tersedia dalam bentuk **Excel** dan **ZIP file**.

## 📧 Kontak

PT Laman Davindo Bahman
🖥️ Sistem Ekstraksi Dokumen Imigrasi
