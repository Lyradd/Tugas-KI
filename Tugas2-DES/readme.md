# Aplikasi Chat Terenkripsi DES (Half-Duplex)

Aplikasi chat client-server sederhana yang mengimplementasikan komunikasi terenkripsi menggunakan algoritma Data Encryption Standard (DES). Komunikasi berjalan secara half-duplex, artinya client dan server mengirim dan menerima pesan secara bergantian (tidak bersamaan).

Aplikasi ini terdiri dari dua skrip utama: `server.py` dan `client.py`.

## Anggota Kelompok

- **Made Daryl Adi Nugraha** (NRP 5025221008)
- **Muhammad Rafi Budi Purnama** (NRP 5025221307)

## Kontribusi Pekerjaan

### Made Daryl Adi Nugraha (NRP 5025221008)
- Mengimplementasikan logika socket untuk `server.py`, termasuk proses binding, listening, dan accepting koneksi.
- Mengintegrasikan kelas `DES_Cipher` pada sisi server untuk proses enkripsi pesan pertama dan dekripsi balasan dari client.
- Menangani logika padding dan unpadding data di sisi server.

### Muhammad Rafi Budi Purnama (NRP 5025221307)
- Mengimplementasikan logika socket untuk `client.py`, termasuk proses connecting ke server.
- Mengintegrasikan kelas `DES_Cipher` pada sisi client untuk proses dekripsi pesan dari server dan enkripsi balasan ke server.
- Menangani logika padding dan unpadding data di sisi client.

## Fitur Utama

- **Enkripsi Simetris**: Komunikasi diamankan menggunakan algoritma DES 64-bit.
- **Komunikasi Half-Duplex**: Server mengirim pesan terlebih dahulu, kemudian client menerima dan membalas.
- **Implementasi OOP**: Logika enkripsi/dekripsi DES dibungkus dalam kelas `DES_Cipher` yang rapi.
- **Penanganan Blok**: Menggunakan padding (PKCS7-style) untuk memastikan data teks murni sesuai dengan ukuran blok DES (8-byte) sebelum enkripsi.
- **Konfigurasi Statis**: Alamat IP (localhost) dan Port (5001) di-hardcode di dalam skrip.

## Cara Kerja

Arsitektur program ini terdiri dari dua bagian utama: **logika Kriptografi (DES)** dan **logika Jaringan (Socket)**.

### 1. Kriptografi (Kelas `DES_Cipher`)

Inti dari enkripsi dan dekripsi dibungkus di dalam kelas `DES_Cipher`.

#### Inisialisasi (`__init__`)
Saat sebuah objek `DES_Cipher` dibuat, ia mengambil kunci 16-karakter hex (contoh: `AABB09182736CCDD`). Kunci ini segera diproses melalui fungsi `_create_key_schedule` untuk menghasilkan 16 round keys (subkunci) yang akan digunakan selama proses enkripsi/dekripsi.

#### Enkripsi (`encrypt_block`)
- Mengambil 1 blok plaintext (8 byte).
- Melakukan padding jika perlu (ditangani oleh fungsi `add_padding` di luar kelas).
- Mengubah teks ke biner dan menerapkan `INITIAL_PERMUTATION`.
- Menjalankan 16 ronde algoritma Feistel, yang melibatkan ekspansi, XOR dengan round key, substitusi S-Box, dan permutasi P-Box.
- Menerapkan `FINAL_PERMUTATION` dan mengubah output biner menjadi hex string 16-karakter.

#### Dekripsi (`decrypt_block`)
- Prosesnya identik dengan enkripsi.
- Perbedaan utamanya adalah round keys yang dihasilkan sebelumnya digunakan dalam urutan terbalik.

### 2. Jaringan (Socket)

Program ini menggunakan modul `socket` standar Python untuk komunikasi TCP/IP.

#### `server.py`
- Membuat socket dan bind ke localhost pada port 5001.
- Menunggu koneksi dari client (`server_socket.accept()`).
- Setelah terhubung, meminta input pesan dari pengguna server.
- Melakukan padding dan mengenkripsi pesan blok per blok menggunakan `cipher.encrypt_block()`.
- Mengirim pesan terenkripsi (sebagai hex string) ke client.
- Menunggu balasan terenkripsi dari client (`conn.recv()`).
- Mendekripsi balasan blok per blok menggunakan `cipher.decrypt_block()`.
- Menghapus padding dan menampilkan pesan asli dari client.
- Menutup koneksi.

#### `client.py`
- Membuat socket dan mencoba terhubung (`client_socket.connect()`) ke server di `localhost:5001`.
- Menunggu pesan terenkripsi dari server (`client_socket.recv()`).
- Mendekripsi pesan blok per blok.
- Menghapus padding dan menampilkan pesan asli dari server.
- Meminta input balasan dari pengguna client.
- Melakukan padding dan mengenkripsi balasan.
- Mengirim balasan terenkripsi ke server.
- Menutup koneksi.

## Prasyarat

- Python 3.x
- Tidak ada library eksternal yang diperlukan (hanya modul standar `socket`)

## Cara Menggunakan

Karena program ini menggunakan localhost, pengujian hanya bisa dilakukan di satu komputer menggunakan dua terminal.

### 1. Buka Terminal 1 (Server)
```bash
python server.py
```

Server akan berjalan dan menampilkan `Chat Server listening on localhost:5001...`. Server akan menunggu koneksi.

### 2. Buka Terminal 2 (Client)
```bash
python client.py
```

### 3. Mulai Chat (Bergantian)

1. **Di Terminal 1 (Server)**: Program akan meminta Anda `Masukkan pesan untuk dikirim:`. Ketik pesan, tekan Enter. Pesan terenkripsi akan dikirim.

2. **Di Terminal 2 (Client)**: Anda akan melihat pesan terenkripsi dari server, diikuti hasil dekripsinya. Program kemudian akan meminta Anda `Masukkan balasan untuk dikirim:`. Ketik balasan, tekan Enter.

3. **Di Terminal 1 (Server)**: Anda akan melihat balasan terenkripsi dari client, diikuti hasil dekripsinya. Program kemudian akan selesai.

## Struktur Project
```
.
├── server.py          # Server-side implementation
├── client.py          # Client-side implementation
└── README.md          # Dokumentasi project
```

