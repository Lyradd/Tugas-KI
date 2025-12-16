# Aplikasi Chat Terenkripsi Hybrid (DES + RSA) dengan Digital Signature

Aplikasi chat ini merupakan implementasi tingkat lanjut dari sistem komunikasi aman yang menggabungkan **Enkripsi Hybrid** (Confidentiality) dan **Digital Signature** (Authentication & Integrity).

Proyek ini adalah evolusi dari **Tugas 3** (Distribusi Kunci), kini diperbarui menjadi **Tugas 4** dengan penambahan mekanisme "Public Key Cryptosystem" untuk menandatangani setiap pesan, memastikan pesan benar-benar berasal dari pengirim asli dan tidak dimanipulasi di tengah jalan.

## 👥 Anggota Kelompok

* **Made Daryl Adi Nugraha** (NRP 5025221008)
* **Muhammad Rafi Budi Purnama** (NRP 5025221307)

## 🛠️ Kontribusi Pekerjaan

### Made Daryl Adi Nugraha (NRP 5025221008)

* Mengimplementasikan modul `RSA.py` dengan fungsi matematika manual (tanpa library eksternal) untuk pembangkitan kunci prima, enkripsi/dekripsi asimetris, serta fungsi *Signing* dan *Verifying*.
* Mengimplementasikan hashing SHA-256 untuk pembuatan *digest* pesan sebelum ditandatangani.
* Menyusun logika verifikasi tanda tangan digital untuk memvalidasi integritas pesan.

### Muhammad Rafi Budi Purnama (NRP 5025221307)

* Mengintegrasikan protokol *Handshake* dua arah pada `client.py` di mana kedua belah pihak (Host & Guest) saling bertukar Public Key.
* Memperbarui struktur paket data pengiriman menjadi format `Encrypted_Message || Digital_Signature`.
* Mengimplementasikan tampilan UI pada terminal untuk menampilkan status verifikasi (`[✅ VERIFIED]` atau `[❌ FAKE]`).

## ✨ Fitur Utama

1.  **Enkripsi Hybrid (Confidentiality)**:
    * Menggunakan **RSA** untuk mendistribusikan kunci sesi secara aman.
    * Menggunakan **DES 64-bit** (ECB/CBC) untuk mengenkripsi isi pesan percakapan agar cepat dan efisien.

2.  **Digital Signature (Authentication & Integrity)**:
    * Setiap pesan yang dikirim ditandatangani menggunakan **RSA Private Key** pengirim.
    * Penerima memverifikasi tanda tangan menggunakan **RSA Public Key** pengirim.
    * Menjamin *Non-Repudiation* (pengirim tidak bisa menyangkal pesan yang dikirim).

3.  **Arsitektur Host-Guest via Relay**:
    * Menggunakan server perantara (*Blind Relay*) yang hanya meneruskan paket, sehingga komunikasi bisa dilakukan antar dua *client* yang berbeda.
    * Mendukung komunikasi **Full-Duplex** (bisa kirim dan terima bersamaan) menggunakan *Multithreading*.

## ⚙️ Cara Kerja Sistem

Aplikasi berjalan melalui beberapa tahapan protokol keamanan:

### 1. Inisialisasi & Handshake (Key Exchange)
Saat aplikasi dimulai, setiap *client* akan membangkitkan pasangan kunci RSA (Privat & Publik) sendiri-sendiri.

1.  **Connect**: Client Host dan Client Guest terhubung ke Relay Server.
2.  **Exchange Public Key**: Host dan Guest saling bertukar **RSA Public Key** masing-masing.
3.  **Session Key Dist**: Host membuat kunci DES (Random 8 byte), mengenkripsinya dengan Public Key Guest, lalu mengirimnya. Guest mendekripsi kunci tersebut dengan Private Key-nya.
    * *Hasil*: Kedua pihak kini memegang Kunci DES yang sama dan Public Key lawan bicara.

### 2. Proses Kirim Pesan (Signing + Encryption)
Ketika pengguna mengirim pesan:
1.  **Hashing**: Sistem membuat hash SHA-256 dari pesan asli.
2.  **Signing**: Hash tersebut dienkripsi menggunakan **Private Key Pengirim** -> menghasilkan *Signature*.
3.  **Encryption**: Pesan asli dienkripsi menggunakan **Kunci DES** -> menghasilkan *Ciphertext*.
4.  **Sending**: Paket dikirim dalam format `Ciphertext || Signature`.

### 3. Proses Terima Pesan (Decryption + Verification)
Ketika pengguna menerima pesan:
1.  **Splitting**: Paket dipisah menjadi *Ciphertext* dan *Signature*.
2.  **Decryption**: *Ciphertext* didekripsi dengan Kunci DES untuk mendapatkan pesan asli.
3.  **Verification**: *Signature* didekripsi menggunakan **Public Key Pengirim** untuk mendapatkan hash, lalu dibandingkan dengan hash pesan asli.
4.  **Result**: Jika cocok, pesan ditampilkan dengan label `[✅ VERIFIED]`.

## 📋 Prasyarat

* Python 3.x
* (Opsional) Modul standar `socket`, `threading`, `random`, `hashlib`. Tidak memerlukan instalasi `pip` tambahan karena menggunakan library bawaan Python.

## ▶️ Cara Menjalankan

Dibutuhkan 3 Terminal untuk simulasi (1 Server Relay, 2 Client).

### 1. Jalankan Server Relay
Buka terminal pertama, arahkan ke folder proyek:

```bash
python server.py
```

Server akan menunggu koneksi pada port 5001.

### 2. Jalankan Client 1 (Sebagai HOST)
Buka terminal kedua:
```bash
python client.py
```

* Pilih opsi 1 (HOST).

* Tunggu proses Generating RSA primes selesai.

* Client akan menunggu partner.

### 3. Jalankan Client 2 (Sebagai GUEST)
Buka terminal ketiga:
```bash
python client.py
```

* Pilih opsi 2 (GUEST).

* Tunggu proses Generating RSA primes selesai.

* Client akan otomatis bertukar kunci dengan Host.

### 4. Mulai Chatting
Setelah muncul pesan Siap Chatting!, silakan ketik pesan di kedua terminal client. Perhatikan label [✅ VERIFIED] yang muncul di sisi penerima.


## 📂 Struktur Proyek
```
├── DES.py             # Implementasi algoritma DES

├── RSA.py             # Implementasi RSA, Keygen, Sign, & Verify

├── server.py          # Relay Server (Meneruskan paket data antar client)

├── client.py          # Program Utama (Logic Chat, Threading, Protocol)

└── README.md          # Dokumentasi
```