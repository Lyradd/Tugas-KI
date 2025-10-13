# Implementasi Algoritma DES (Data Encryption Standard)

## Informasi Penulis

-   **Nama:** Made Daryl Adi Nugraha
-   **NRP:** 5025221008

---

## Deskripsi Proyek

Proyek ini adalah sebuah implementasi sederhana dari algoritma kriptografi **Data Encryption Standard (DES)** menggunakan bahasa pemrograman Python. Program ini dirancang untuk tujuan edukasi, dengan menampilkan setiap langkah proses secara detail, mulai dari pembuatan subkunci (*key generation*) hingga proses enkripsi dan dekripsi blok data 64-bit.

---

## Fitur Utama

-   **Enkripsi DES**: Mengubah *plaintext* 64-bit menjadi *ciphertext* 64-bit menggunakan kunci 64-bit.
-   **Dekripsi DES**: Mengembalikan *ciphertext* menjadi *plaintext* asli menggunakan kunci yang sama.
-   **Output Detail**: Menampilkan output langkah-demi-langkah untuk setiap proses, termasuk:
    -   Permutasi awal (IP) dan akhir (FP).
    -   Proses pembuatan 16 *subkeys*.
    -   Detail setiap 16 ronde dalam jaringan Feistel.
-   **Input Heksadesimal**: Menerima input *plaintext* dan kunci dalam format heksadesimal (16 karakter).

---

## Cara Penggunaan

1.  Pastikan Anda telah menginstal Python di komputer Anda.
2.  Simpan kode di atas sebagai file Python (contoh: `des_manual.py`).
3.  Jalankan program melalui terminal atau *command prompt*:
    ```bash
    python des_manual.py
    ```
4.  Ikuti instruksi yang muncul di layar untuk memasukkan **Plaintext** dan **Kunci**, masing-masing dalam 16 karakter heksadesimal.
    -   Contoh Plaintext: `0123456789ABCDEF`
    -   Contoh Kunci: `133457799BBCDFF1`
5.  Program akan secara otomatis menjalankan proses enkripsi, lalu dekripsi, dan menampilkan hasilnya beserta verifikasi.