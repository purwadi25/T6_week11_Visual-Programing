# T6 Week 11 - Post Manager REST API

## Identitas
- Nama : Bagas
- NIM : F1D02310115
- Kelas : Grup 15

---

## Deskripsi Project
Project ini merupakan aplikasi desktop CRUD Post Manager menggunakan Python Tkinter yang terhubung dengan REST API.

Aplikasi mampu melakukan:
- Menampilkan semua data post
- Menampilkan detail post
- Menambah post baru
- Mengedit post
- Menghapus post
- Multi-threading agar UI tidak freeze saat request API berjalan
- Error handling dan loading state

API yang digunakan:
```text
https://api.pahrul.my.id/api/posts
```

---

## Teknologi yang Digunakan
- Python
- Tkinter
- Requests
- Threading
- REST API

---

## Fitur Aplikasi
### ✅ GET Posts
Menampilkan seluruh data posts ke dalam tabel.

### ✅ Detail Post
Menampilkan detail lengkap post saat baris dipilih.

### ✅ Tambah Post
Menambahkan data post baru menggunakan HTTP POST.

### ✅ Edit Post
Mengubah data post menggunakan HTTP PUT.

### ✅ Hapus Post
Menghapus post menggunakan HTTP DELETE dengan konfirmasi dialog.

### ✅ Threading
Semua request API dijalankan di thread terpisah agar aplikasi tetap responsif.

### ✅ Error Handling
Menangani:
- Timeout
- Connection Error
- Validasi slug duplicate (422)

---

## Cara Menjalankan Program

### 1. Install Dependency
```bash
pip install requests
```

### 2. Jalankan Program
```bash
python T6_week_11.py
```

---

# Screenshot Aplikasi

## Tampilan Awal
![Tampilan Awal](Screenshot/Tampilan_Awal.png)

---

## Tambah Post
![Tambah Post](Screenshot/Tambah_Posh.png)

---

## Edit Post
![Edit Post](Screenshot/Edit_Posh.png)

---

## Hapus Post
![Hapus Post](Screenshot/Hapus_Posh.png)

---

## Struktur Folder
```text
T6-week11/
│
├── T6_week_11.py
├── README.md
├── Screenshot/
│   ├── Tampilan_Awal.png
│   ├── Tambah_Posh.png
│   ├── Edit_Posh.png
│   └── Hapus_Posh.png
```

---

## Hasil
Aplikasi berhasil mengimplementasikan CRUD lengkap menggunakan REST API dengan multi-threading sehingga UI tetap responsif selama proses request berlangsung.
