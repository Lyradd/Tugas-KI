# 1. Initial Permutation (IP)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# 2. Final Permutation (FP) atau Inverse Initial Permutation (IP^-1)
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

# 3. Expansion Box (E-box) - untuk memperluas 32-bit menjadi 48-bit
E_BOX = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

# 4. Substitution Boxes (S-boxes) - 8 S-box
S_BOXES = [
    # S-box 1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S-box 2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S-box 3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S-box 4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S-box 5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S-box 6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S-box 7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S-box 8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# 5. Permutation Box (P-box)
P_BOX = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

# --- Tabel untuk Proses Pembuatan Kunci ---

# 6. Permuted Choice 1 (PC-1)
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# 7. Permuted Choice 2 (PC-2)
PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

# 8. Jadwal Pergeseran Kiri (Left Shift) untuk setiap ronde
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# --- Fungsi-Fungsi Pembantu ---

def hex_to_bits(hex_str):
    """Mengubah string heksadesimal menjadi list of bits (0 atau 1)."""
    return [int(b) for c in hex_str for b in bin(int(c, 16))[2:].zfill(4)]

def bits_to_hex(bits):
    """Mengubah list of bits kembali menjadi string heksadesimal."""
    return "".join([hex(int("".join(map(str, bits[i:i+4])), 2))[2:].upper() for i in range(0, len(bits), 4)])

def permute(block, table):
    """Melakukan permutasi pada blok bit berdasarkan tabel yang diberikan."""
    return [block[i - 1] for i in table]

def xor(bits1, bits2):
    """Melakukan operasi XOR antara dua list of bits."""
    return [bit1 ^ bit2 for bit1, bit2 in zip(bits1, bits2)]

def left_shift(bits, n):
    """Melakukan pergeseran sirkular ke kiri."""
    return bits[n:] + bits[:n]

# --- Fungsi-Fungsi Inti DES ---

def generate_subkeys(key_bits, verbose=False):
    """Menghasilkan 16 subkunci dari kunci utama dengan output detail."""
    key_permuted = permute(key_bits, PC1)
    if verbose:
        print(f"\nSetelah Permuted Choice 1 (PC-1): {bits_to_hex(key_permuted)}")

    C = key_permuted[:28]
    D = key_permuted[28:]
    if verbose:
        print(f"C0: {bits_to_hex(C)}, D0: {bits_to_hex(D)}")
        print("-" * 60)
        print("Ronde\tShift\tCn\t\tDn\t\tSubkunci (K)")
        print("-" * 60)

    subkeys = []
    for i, shift_amount in enumerate(SHIFT_SCHEDULE):
        C = left_shift(C, shift_amount)
        D = left_shift(D, shift_amount)
        
        combined_key = C + D
        subkey = permute(combined_key, PC2)
        subkeys.append(subkey)
        
        if verbose:
            print(f"{i+1:2d}\t{shift_amount}\t{bits_to_hex(C)}\t{bits_to_hex(D)}\t{bits_to_hex(subkey)}")
    
    return subkeys

def feistel_function(right_half, subkey):
    """Implementasi fungsi Feistel (F-function)."""
    # 1. Expansion
    expanded = permute(right_half, E_BOX)
    
    # 2. Key mixing (XOR)
    xored = xor(expanded, subkey)
    
    # 3. Substitution (S-boxes)
    sbox_output = []
    for i in range(8):
        chunk = xored[i*6 : (i+1)*6]
        row = int(str(chunk[0]) + str(chunk[5]), 2)
        col = int("".join(map(str, chunk[1:5])), 2)
        val = S_BOXES[i][row][col]
        sbox_output.extend([int(b) for b in bin(val)[2:].zfill(4)])

    # 4. Permutation (P-box)
    permuted_output = permute(sbox_output, P_BOX)
    
    return permuted_output

def des_algorithm(block_bits, subkeys, is_decrypt=False, verbose=False):
    """Proses utama DES untuk satu blok 64-bit dengan output detail."""
    # 1. Initial Permutation
    permuted_block = permute(block_bits, IP)
    if verbose:
        print(f"\nSetelah Initial Permutation (IP): {bits_to_hex(permuted_block)}")

    # 2. Pisahkan menjadi bagian kiri (L) dan kanan (R)
    L = permuted_block[:32]
    R = permuted_block[32:]
    if verbose:
        print(f"L0: {bits_to_hex(L)}, R0: {bits_to_hex(R)}")
        print("-" * 60)
        print("Ronde\tL(n)\t\tR(n)\t\tSubkunci (K)")
        print("-" * 60)

    # Gunakan subkunci terbalik untuk dekripsi
    if is_decrypt:
        subkeys = subkeys[::-1]

    # 3. 16 Ronde Feistel
    for i in range(16):
        if verbose:
            print(f"{i+1:2d}\t{bits_to_hex(L)}\t{bits_to_hex(R)}\t{bits_to_hex(subkeys[i])}")
            
        L_next = R
        f_result = feistel_function(R, subkeys[i])
        R_next = xor(L, f_result)
        
        L = L_next
        R = R_next
        
    # 4. Gabungkan kembali (tapi R sebelum L)
    combined = R + L
    if verbose:
        print(f"\nSetelah 16 Ronde (R16 L16): {bits_to_hex(combined)}")
    
    # 5. Final Permutation
    final_block = permute(combined, FP)
    if verbose:
        print(f"Setelah Final Permutation (FP): {bits_to_hex(final_block)}")

    return final_block

# --- Fungsi Utama ---
if __name__ == "__main__":
    print("--- Implementasi DES Manual ---")

    # Ambil input dari pengguna
    while True:
        pt_hex = input("Masukkan Plaintext (16 karakter hex, cth: 0123456789ABCDEF): ").upper()
        if len(pt_hex) == 16 and all(c in '0123456789ABCDEF' for c in pt_hex):
            break
        print("Input tidak valid. Harap masukkan 16 karakter heksadesimal.")

    while True:
        key_hex = input("Masukkan Kunci (16 karakter hex, cth: 133457799BBCDFF1): ").upper()
        if len(key_hex) == 16 and all(c in '0123456789ABCDEF' for c in key_hex):
            break
        print("Input tidak valid. Harap masukkan 16 karakter heksadesimal.")

    # Konversi input ke list of bits
    plaintext_bits = hex_to_bits(pt_hex)
    key_bits = hex_to_bits(key_hex)

    # --- PROSES ENKRIPSI ---
    print("\n" + "="*25 + " PROSES ENKRIPSI " + "="*24)
    print(f"\nPlaintext (hex): {pt_hex}")
    print(f"Kunci (hex)    : {key_hex}")

    print("\n--- 1. Pembuatan Subkunci ---")
    subkeys_enc = generate_subkeys(key_bits, verbose=True)

    print("\n--- 2. Proses Enkripsi Blok ---")
    encrypted_bits = des_algorithm(plaintext_bits, subkeys_enc, is_decrypt=False, verbose=True)
    cipher_text_hex = bits_to_hex(encrypted_bits)
    print("\n================ HASIL ENKRIPSI ================")
    print(f"CIPHERTEXT (HEX): {cipher_text_hex}")
    print("==============================================")

    # --- PROSES DEKRIPSI ---
    print("\n\n" + "="*25 + " PROSES DEKRIPSI " + "="*24)
    print(f"\nCiphertext (hex): {cipher_text_hex}")
    print(f"Kunci (hex)     : {key_hex}")

    print("\n--- 1. Pembuatan Subkunci (sama seperti enkripsi) ---")
    # Kunci yang sama digunakan, urutannya akan dibalik di dalam fungsi des_algorithm
    subkeys_dec = generate_subkeys(key_bits, verbose=True) 
    print("\nCATATAN: Untuk dekripsi, urutan subkunci di atas akan digunakan secara terbalik (K16, K15, ..., K1).")

    print("\n--- 2. Proses Dekripsi Blok ---")
    decrypted_bits = des_algorithm(encrypted_bits, subkeys_dec, is_decrypt=True, verbose=True)
    plain_text_hex = bits_to_hex(decrypted_bits)
    print("\n================ HASIL DEKRIPSI ================")
    print(f"PLAINTEXT (HEX): {plain_text_hex}")
    print("==============================================")

    # Verifikasi
    if pt_hex == plain_text_hex:
        print("\n\nVerifikasi Berhasil: Plaintext asli sama dengan hasil dekripsi.")
    else:
        print("\n\nVerifikasi Gagal: Terjadi kesalahan dalam proses.")

