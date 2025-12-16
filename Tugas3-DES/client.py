# client.py
import socket
import threading
import os
import binascii
import sys
import DES 
import RSA

HEADER_PUBKEY = b"PUBKEY::"  
HEADER_SECRET = b"SECRET::" 
HEADER_MSG    = b"MSG::"     

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cipher = None  
        self.is_host = False
        self.rsa_private = None
        self.stop_thread = False

    def start(self):
        print("--- APLIKASI CHAT E2EE (End-to-End Encryption) ---")
        role = input("Pilih Peran:\n1. Buat Room Baru (HOST)\n2. Join Room (GUEST)\nPilihan (1/2): ")
        
        target_ip = '10.203.199.182'
        self.sock.connect((target_ip, 5001))
        print(f"[*] Terhubung ke Relay Server di {target_ip}:5001")

        recv_thread = threading.Thread(target=self.receive_handler)
        recv_thread.daemon = True
        recv_thread.start()

        if role == '1':
            self.setup_as_host()
        else:
            self.setup_as_guest()

        # Loop Utama: Mengirim Pesan
        self.input_loop()

    def setup_as_host(self):
        """Host membuat Kunci DES dan membagikannya ke yang request."""
        self.is_host = True
        # 1. Buat Kunci DES Master
        des_key_bytes = os.urandom(8)
        secret_key_hex = binascii.hexlify(des_key_bytes).decode('utf-8').upper()
        
        # 2. Inisialisasi Cipher
        self.cipher = DES.DES_Cipher(secret_key_hex)
        print(f"\n[HOST] Room dibuat. Kunci DES Master: {secret_key_hex}")
        print("[HOST] Menunggu user lain join...")

    def setup_as_guest(self):
        """Guest membuat RSA Keypair dan minta Kunci DES ke Host."""
        self.is_host = False
        print("\n[GUEST] Menghasilkan pasangan kunci RSA...")
        self.rsa_private, pub_pem = RSA.generate_rsa_keypair()
        
        print("[GUEST] Mengirim Kunci Publik ke Host...")
        payload = HEADER_PUBKEY + pub_pem
        self.sock.sendall(payload)
        
        print("[GUEST] Menunggu Kunci DES dari Host (dienkripsi RSA)...")

    def receive_handler(self):
        """Thread yang selalu berjalan untuk memproses data masuk."""
        while not self.stop_thread:
            try:
                data = self.sock.recv(4096)
                if not data: break
                if data.startswith(HEADER_PUBKEY):
                    if self.is_host:
                        public_key_pem = data[len(HEADER_PUBKEY):]
                        print("\n[HOST] Menerima request join (Public Key). Mengirim Kunci DES...")
                        
                        # Ambil Kunci DES kita (dari properti cipher.round_keys agak ribet, 
                        # jadi kita simpan hex manual atau ambil dari input awal. 
                        # Di sini kita asumsi kita regenerate dari cipher object tidak bisa, 
                        # jadi simplifikasi: Host harus simpan raw key.
                        # (NOTE: Untuk simplifikasi kode tugas, kita asumsikan Host 
                        # tidak perlu menyimpan variabel 'key' terpisah jika kita bisa akses,
                        # tapi cara paling aman adalah simpan di attribute saat init).
                        
                        # *Revisi*: Di setup_as_host, kita simpan kunci aslinya? 
                        # Tidak perlu, kita generate kunci baru saja tidak bisa. 
                        # Solusi: Cipher DES Anda menyimpan round_keys, bukan master key.
                        # Agar aman, Host kita ubah sedikit untuk simpan 'self.master_key_bytes'
                        pass 

                elif data.startswith(HEADER_SECRET):
                    if not self.is_host and self.cipher is None:
                        encrypted_key = data[len(HEADER_SECRET):]
                        try:
                            # Dekripsi menggunakan Kunci Privat Guest
                            des_key_bytes = RSA.decrypt_secret_key(encrypted_key, self.rsa_private)
                            secret_key_hex = binascii.hexlify(des_key_bytes).decode('utf-8').upper()
                            
                            # Inisialisasi Cipher
                            self.cipher = DES.DES_Cipher(secret_key_hex)
                            print(f"\n[GUEST] Sukses! Kunci DES diterima: {secret_key_hex}")
                            print("--- SIAP CHATTING ---")
                            print("Client: ", end="", flush=True)
                        except Exception as e:

                            pass 

                # KASUS 3: Pesan Chat Biasa (Semua peduli)
                elif data.startswith(HEADER_MSG):
                    if self.cipher: # Hanya jika sudah punya kunci
                        encrypted_msg_str = data[len(HEADER_MSG):].decode('utf-8')
                        
                        # Dekripsi Pesan
                        decrypted_padded = ""
                        for i in range(0, len(encrypted_msg_str), 16):
                            block = encrypted_msg_str[i:i+16]
                            if len(block) == 16:
                                decrypted_padded += self.cipher.decrypt_block(block)
                        
                        final_msg = DES.remove_padding(decrypted_padded)
                        print(f"\rTeman: {final_msg}\nClient: ", end="", flush=True)

            except Exception as e:
                # print(f"Error recv: {e}")
                break

    def input_loop(self):
        pass

def run_chat_client_full():
    client = ChatClientFull()
    client.start()

class ChatClientFull:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cipher = None
        self.is_host = False
        self.rsa_private = None
        self.master_key_bytes = None
        self.stop_thread = False

    def start(self):
        print("--- CLIENT E2EE ---")
        role = input("1. HOST (Buat Room)\n2. GUEST (Join Room)\nPilih: ")
        self.sock.connect(('localhost', 5001))
        
        recv_thread = threading.Thread(target=self.receive_handler)
        recv_thread.daemon = True
        recv_thread.start()

        if role == '1':
            self.is_host = True
            self.master_key_bytes = os.urandom(8)
            hex_key = binascii.hexlify(self.master_key_bytes).decode('utf-8').upper()
            self.cipher = DES.DES_Cipher(hex_key)
            print(f"[HOST] Ready. Key: {hex_key}")
        else:
            self.is_host = False
            self.rsa_private, pub_pem = RSA.generate_rsa_keypair()
            self.sock.sendall(HEADER_PUBKEY + pub_pem)
            print("[GUEST] Waiting for key...")
            while self.cipher is None:
                pass

        # Loop Chat
        print("\n--- MULAI CHAT (Ketik 'stop' untuk keluar) ---")
        while True:
            msg = input("Client: ")
            if msg.lower() == 'stop':
                break
            
            if self.cipher:
                padded = DES.add_padding(msg)
                enc_hex = ""
                for i in range(0, len(padded), 8):
                    enc_hex += self.cipher.encrypt_block(padded[i:i+8])
                
                self.sock.sendall(HEADER_MSG + enc_hex.encode('utf-8'))

        self.sock.close()

    def receive_handler(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data: break

                if data.startswith(HEADER_PUBKEY):
                    if self.is_host:
                        pub_pem = data[len(HEADER_PUBKEY):]
                        enc_key = RSA.encrypt_secret_key(self.master_key_bytes, pub_pem)
                        self.sock.sendall(HEADER_SECRET + enc_key)
                        print("\n[SYSTEM] Member baru bergabung. Kunci dikirim.")
                        print("Client: ", end="", flush=True)

                elif data.startswith(HEADER_SECRET):
                    if not self.is_host and self.cipher is None:
                        try:
                            enc_bytes = data[len(HEADER_SECRET):]
                            key_bytes = RSA.decrypt_secret_key(enc_bytes, self.rsa_private)
                            hex_key = binascii.hexlify(key_bytes).decode('utf-8').upper()
                            self.cipher = DES.DES_Cipher(hex_key)
                            print(f"\n[SYSTEM] Kunci diterima!")
                        except:
                            pass

                elif data.startswith(HEADER_MSG):
                    if self.cipher:
                        enc_str = data[len(HEADER_MSG):].decode('utf-8')
                        dec_padded = ""
                        for i in range(0, len(enc_str), 16):
                            dec_padded += self.cipher.decrypt_block(enc_str[i:i+16])
                        msg = DES.remove_padding(dec_padded)
                        print(f"\rTeman: {msg}\nClient: ", end="", flush=True)
            except:
                break

if __name__ == "__main__":
    run_chat_client_full()