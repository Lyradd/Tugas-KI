# Aplikasi Chat Terenkripsi Hybrid (DES + RSA)

Aplikasi chat client-server ini mengimplementasikan enkripsi *hybrid*. Proyek ini merupakan evolusi dari **Tugas 2** (yang menggunakan kunci DES *hardcoded*) dengan menerapkan solusi **Tugas 3**, yaitu "distribusi kunci publik untuk kunci rahasia".

Aplikasi ini tidak lagi menyimpan kunci rahasia di dalam kode. Sebaliknya, ia menggunakan RSA (asimetris) untuk secara aman membuat dan mendistribusikan kunci DES (simetris) yang unik untuk setiap sesi chat.

## 👥 Anggota Kelompok

* **Made Daryl Adi Nugraha** (NRP 5025221008)
* **Muhammad Rafi Budi Purnama** (NRP 5025221307)

## 🛠️ Kontribusi Pekerjaan

### Made Daryl Adi Nugraha (NRP 5025221008)

* Mengimplementasikan modul `RSA.py` menggunakan *library* `cryptography` untuk enkripsi/dekripsi asimetris.
* Memperbarui `server.py` untuk menghasilkan *key pair* RSA, mengirim kunci publik, dan mendekripsi kunci DES rahasia yang diterima.
* Mengimplementasikan logika *looping chat* (`while True`) di sisi server.

### Muhammad Rafi Budi Purnama (NRP 5025221307)

* Melakukan modularisasi kode dengan memindahkan kelas `DES_Cipher` dan fungsi *padding* ke file terpisah `DES.py`.
* Memperbarui `client.py` untuk menerima kunci publik, membuat kunci DES acak (`os.urandom`), dan mengenkripsinya sebelum dikirim.
* Mengimplementasikan logika *looping chat* (`while True`) di sisi klien.

## ✨ Fitur Utama

* **Enkripsi Hybrid**: Menggunakan **RSA-2048** (asimetris) untuk pertukaran kunci yang aman dan **DES** (simetris) untuk enkripsi percakapan yang cepat.
* **Distribusi Kunci Dinamis**: Kunci DES tidak lagi di-*hardcode*. Kunci rahasia baru dibuat secara acak oleh klien untuk setiap sesi.
* **Struktur Modular**: Logika dipisahkan menjadi empat file: `server.py`, `client.py`, `DES.py`, dan `RSA.py`.
* **Komunikasi Full-Duplex**: Sesi chat kini berjalan dalam *loop* `while True`, memungkinkan percakapan bolak-balik hingga salah satu pengguna mengetik `stop`.

## ⚙️ Cara Kerja

Aplikasi berjalan dalam dua fase utama:

### 1. Fase Pertukaran Kunci (Tugas 3)

Fase ini terjadi otomatis saat klien pertama kali terhubung untuk menetapkan kunci rahasia (DES).

1.  **Server** membuat sepasang kunci **RSA Privat & Publik** (`generate_rsa_keypair`).
2.  **Klien** terhubung ke server.
3.  **Server** mengirimkan **Kunci Publik** RSA-nya (dalam format PEM) ke Klien.
4.  **Klien** menerima Kunci Publik server.
5.  **Klien** membuat **Kunci DES 64-bit** baru secara acak (`os.urandom(8)`).
6.  **Klien** menggunakan **Kunci Publik** server untuk *mengenkripsi* Kunci DES acak tadi (`encrypt_secret_key`).
7.  **Klien** mengirim Kunci DES yang sudah terenkripsi ini ke Server.
8.  **Server** menerima paket dan menggunakan **Kunci Privat** RSA-nya untuk *mendekripsi* paket tersebut (`decrypt_secret_key`).

**Hasil:** Server dan Klien kini sama-sama memiliki Kunci DES rahasia (`SECRET_KEY_HEX`) yang sama untuk sesi ini.

### 2. Fase Sesi Chat (Tugas 2 yang Diperbarui)

Setelah kunci DES aman di kedua sisi, percakapan terenkripsi dimulai.

1.  Seluruh percakapan dienkripsi dan didekripsi menggunakan `DES_Cipher` dari `DES.py`.
2.  Server dan Klien masuk ke dalam `while True`.
3.  Server mengirim pesan, Klien menerima dan mendekripsi.
4.  Klien membalas, Server menerima dan mendekripsi.
5.  Proses ini berulang sampai salah satu pihak mengetik `stop` untuk mengakhiri sesi.

## 📋 Prasyarat

* Python 3.x
* Library `cryptography` (diimpor di `RSA.py`)

## ▶️ Cara Menjalankan

Berikut adalah langkah-langkah untuk menjalankan aplikasi ini:

### 1. Persiapan Awal (Hanya sekali)

a. Pastikan keempat file (`DES.py`, `RSA.py`, `server.py`, `client.py`) berada di dalam folder yang sama.

b. Buka terminal Anda dan instal *library* `cryptography` yang diperlukan oleh `RSA.py`:

    ```
    pip install cryptography
    ```

### 2. Jalankan Server

a. Buka **Terminal 1** (atau Command Prompt).

b. Arahkan ke folder tempat Anda menyimpan file-file proyek.

c. Jalankan `server.py`:

    ```
    python server.py
    ```

d. Server akan berjalan dan menampilkan `Chat Server listening on 0.0.0.0:5001...`. Server akan diam dan menunggu koneksi.

### 3. Jalankan Klien

a. Buka **Terminal 2** (biarkan Terminal 1 tetap berjalan).

b. Arahkan ke folder yang **sama**.

c. Jalankan `client.py`:

    ```
    python client.py
    ```

d. Klien akan otomatis terhubung, melakukan pertukaran kunci, dan menampilkan `--- Sesi Chat Dimulai ---`. Ia akan menunggu pesan pertama dari server.

### 4. Mulai Percakapan

a. Kembali ke **Terminal 1 (Server)**. Masukkan pesan pertama Anda di prompt `Server: ` dan tekan Enter.

b. Pindah ke **Terminal 2 (Klien)**. Anda akan melihat pesan dari server. Masukkan balasan Anda di prompt `Client: ` dan tekan Enter.

c. Percakapan akan berlanjut bolak-balik.

d. Untuk berhenti, ketik `stop` di salah satu terminal.


## 📂 Struktur Proyek
├── DES.py             # Modul enkripsi simetris DES

├── RSA.py             # Modul helper enkripsi asimetris RSA

├── server.py          # Skrip utama Server

├── client.py          # Skrip utama Client

└── README.md          # Dokumentasi ini