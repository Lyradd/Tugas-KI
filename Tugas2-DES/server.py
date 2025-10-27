import socket

class DES_Cipher:
    INITIAL_PERMUTATION = [
        58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
    ]
    
    FINAL_PERMUTATION = [
        40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
    ]
    
    EXPANSION_TABLE = [
        32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
    ]
    
    S_BOXES = [
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]
    
    PERMUTATION_P = [
        16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
    ]
    
    PC1_TABLE = [
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
    ]
    
    PC2_TABLE = [
        14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
    ]
    
    SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # --- 2. Inisialisasi Kelas ---
    def __init__(self, hex_key):
        """Saat objek dibuat, langsung generate subkunci."""
        # Konversi key hex ke format string biner 64-bit
        key_bytes = bytes.fromhex(hex_key).decode('latin-1')
        key_binary_str = self._text_to_binary_str(key_bytes)
        # Simpan subkunci yang sudah digenerate
        self.round_keys = self._create_key_schedule(key_binary_str)

    # --- 3. Fungsi Internal (Private Methods) ---
    def _apply_permutation(self, binary_str, table):
        """Fungsi 'permute'"""
        return "".join([binary_str[i - 1] for i in table])

    def _left_shift(self, binary_str, count):
        """Fungsi 'shift_left'"""
        return binary_str[count:] + binary_str[:count]

    def _xor_binary_strings(self, s1, s2):
        """Helper baru untuk XOR dua string biner."""
        length = len(s1)
        int1 = int(s1, 2)
        int2 = int(s2, 2)
        return bin(int1 ^ int2)[2:].zfill(length)

    def _feistel_function(self, right_32bit, key_48bit):
        """Logika F-function (E, XOR, S-Box, P) yang ada di dalam loop encrypt/decrypt."""
        # Expansion D-box
        expanded_right = self._apply_permutation(right_32bit, self.EXPANSION_TABLE)
        
        # XOR dengan subkunci
        sbox_input = self._xor_binary_strings(expanded_right, key_48bit)
        
        # S-box
        sbox_output_str = ""
        for j in range(8):
            chunk = sbox_input[j*6:(j*6)+6]
            row = int(chunk[0] + chunk[5], 2)
            col = int(chunk[1:5], 2)
            val = self.S_BOXES[j][row][col]
            sbox_output_str += format(val, '04b')
            
        # Permutasi P
        return self._apply_permutation(sbox_output_str, self.PERMUTATION_P)

    def _create_key_schedule(self, key_64bit_str):
        """Fungsi 'generate_keys'"""
        key_56bit = self._apply_permutation(key_64bit_str, self.PC1_TABLE)
        
        left_key = key_56bit[0:28]
        right_key = key_56bit[28:56]
        
        subkeys = []
        for i in range(16):
            left_key = self._left_shift(left_key, self.SHIFT_SCHEDULE[i])
            right_key = self._left_shift(right_key, self.SHIFT_SCHEDULE[i])
            
            combined_key = left_key + right_key
            round_key = self._apply_permutation(combined_key, self.PC2_TABLE)
            subkeys.append(round_key)
            
        return subkeys

    # --- 4. Fungsi Konversi (Helper) ---
    def _text_to_binary_str(self, text):
        """Fungsi 'string_to_binary'"""
        return "".join(format(ord(char), '08b') for char in text)

    def _binary_str_to_hex(self, binary_str):
        """Fungsi 'binary_to_hex'"""
        return hex(int(binary_str, 2))[2:].upper().zfill(16)
        
    def _hex_to_binary_str(self, hex_str):
        """Fungsi 'hex_to_binary'"""
        return bin(int(hex_str, 16))[2:].zfill(64)
        
    def _binary_str_to_text(self, binary_str):
        """Fungsi 'binary_to_string'"""
        text = ""
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i+8]
            text += chr(int(byte, 2))
        return text

    # --- 5. Fungsi Publik (Public Methods) ---
    def encrypt_block(self, plaintext_block):
        """Fungsi 'encrypt', tapi untuk 1 blok 8-byte."""
        binary_data = self._text_to_binary_str(plaintext_block)
        binary_data = self._apply_permutation(binary_data, self.INITIAL_PERMUTATION)
        
        left = binary_data[0:32]
        right = binary_data[32:64]
        
        for i in range(16):
            round_key = self.round_keys[i]
            f_result = self._feistel_function(right, round_key)
            
            # Operasi XOR
            new_left = self._xor_binary_strings(left, f_result)
            left = new_left
            
            # Swap, kecuali ronde terakhir
            if i != 15:
                left, right = right, left
                
        # Kombinasi dan permutasi final
        combined_block = left + right
        cipher_binary = self._apply_permutation(combined_block, self.FINAL_PERMUTATION)
        return self._binary_str_to_hex(cipher_binary)

    def decrypt_block(self, hex_ciphertext_block):
        """Fungsi 'decrypt', tapi untuk 1 blok 16-hex."""
        binary_data = self._hex_to_binary_str(hex_ciphertext_block)
        binary_data = self._apply_permutation(binary_data, self.INITIAL_PERMUTATION)
        
        left = binary_data[0:32]
        right = binary_data[32:64]
        
        decryption_keys = self.round_keys[::-1] 
        
        for i in range(16):
            round_key = decryption_keys[i]
            f_result = self._feistel_function(right, round_key)
            
            new_left = self._xor_binary_strings(left, f_result)
            left = new_left
            
            if i != 15:
                left, right = right, left
                
        # Kombinasi dan permutasi final
        combined_block = left + right
        plain_binary = self._apply_permutation(combined_block, self.FINAL_PERMUTATION)
        return self._binary_str_to_text(plain_binary)

# --- End of DES_Cipher Class ---

# --- Fungsi Padding (PKCS7-style) ---
def add_padding(text_data):
    block_size = 8  # DES block size is 8 bytes
    padding_len = block_size - (len(text_data) % block_size)
    padding_char = chr(padding_len)
    return text_data + (padding_char * padding_len)

def remove_padding(text_data):
    """Fungsi baru untuk menghapus padding."""
    padding_len = ord(text_data[-1])
    if padding_len > 8:
        return text_data # Bukan padding yang valid
    return text_data[:-padding_len]

# --- Logika Utama Socket Server ---
def run_chat_server():
    HOST_ADDRESS = '0.0.0.0'  
    PORT_NUMBER = 5001
    SECRET_KEY_HEX = "AABB09182736CCDD" 
    
    # 1. Buat satu objek cipher
    try:
        cipher = DES_Cipher(SECRET_KEY_HEX)
        print("DES Cipher object initialized successfully.")
    except Exception as e:
        print(f"Error initializing cipher (check key hex format): {e}")
        return

    # 2. Setup koneksi socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST_ADDRESS, PORT_NUMBER))
        server_socket.listen(1)
        print(f"Chat Server listening on {HOST_ADDRESS}:{PORT_NUMBER}...")
        
        # Terima koneksi
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connection established with {addr}")
            try:
                # --- Sesi Kirim Pesan Pertama ---
                message_to_send = input("Masukkan pesan untuk dikirim: ")
                padded_message = add_padding(message_to_send)
                
                encrypted_hex_output = ""
                # Enkripsi per blok 8-byte
                for i in range(0, len(padded_message), 8):
                    block = padded_message[i:i+8]
                    encrypted_hex_output += cipher.encrypt_block(block)
                    
                print(f"Mengirim data terenkripsi: {encrypted_hex_output}")
                conn.sendall(encrypted_hex_output.encode('utf-8'))
                
                # --- Sesi Terima Balasan ---
                encrypted_response = conn.recv(1024).decode('utf-8')
                if not encrypted_response:
                    raise ConnectionError("Client disconnected.")
                    
                print(f"Menerima data terenkripsi: {encrypted_response}")
                
                decrypted_response_padded = ""
                # Dekripsi per blok 16-hex
                for i in range(0, len(encrypted_response), 16):
                    hex_block = encrypted_response[i:i+16]
                    decrypted_response_padded += cipher.decrypt_block(hex_block)
                    
                # Hapus padding
                final_response = remove_padding(decrypted_response_padded)
                print(f"Hasil Dekripsi: {final_response}")
                
            except Exception as e:
                print(f"An error occurred during chat: {e}")

# --- Jalankan Program ---
if __name__ == "__main__":
    run_chat_server()