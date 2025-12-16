import socket
import threading
import os
import binascii
import DES 
import RSA

# --- Header Protokol ---
HEADER_PUBKEY = b"PUBKEY::" 
HEADER_SECRET = b"SECRET::"
HEADER_MSG    = b"MSG::"

class ChatClientFull:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.des_cipher = None
        self.is_host = False
        
        self.my_rsa_private = None
        self.my_rsa_public_pem = None
        
        self.partner_rsa_public_pem = None
        
        self.master_key_bytes = None
        self.stop_thread = False

    def start(self):
        print("--- APLIKASI CHAT: HYBRID ENCRYPTION + DIGITAL SIGNATURE ---")
        print("[Ref: Public-Key Cryptosystems Diagram]")
        role = input("1. HOST (Buat Room)\n2. GUEST (Join Room)\nPilih: ")
        
        print("\n[INIT] Membuat pasangan kunci RSA & Signature (Mohon tunggu)...")
        self.my_rsa_private, self.my_rsa_public_pem = RSA.generate_rsa_keypair()
        print("[INIT] Kunci RSA siap.")

        target_ip = 'localhost' # buat testing pake localhost aja
        try:
            self.sock.connect((target_ip, 5001))
            print(f"[*] Terhubung ke Relay Server di {target_ip}:5001")
        except:
            print("[!] Gagal connect ke server. Pastikan server.py sudah jalan.")
            return

        recv_thread = threading.Thread(target=self.receive_handler)
        recv_thread.daemon = True
        recv_thread.start()

        print("[HANDSHAKE] Mengirim Public Key saya ke partner...")
        self.sock.sendall(HEADER_PUBKEY + self.my_rsa_public_pem)

        if role == '1':
            self.setup_as_host()
        else:
            self.setup_as_guest()
        self.chat_loop()

    def setup_as_host(self):
        self.is_host = True
        self.master_key_bytes = os.urandom(8)
        hex_key = binascii.hexlify(self.master_key_bytes).decode('utf-8').upper()
        self.des_cipher = DES.DES_Cipher(hex_key)
        print(f"\n[HOST] Kunci DES Master dibuat: {hex_key}")
        print("[HOST] Menunggu Public Key dari Guest untuk mengirim Kunci DES...")

    def setup_as_guest(self):
        self.is_host = False
        print("\n[GUEST] Menunggu Kunci DES dari Host...")

    def chat_loop(self):
        print("\n--- MULAI CHAT (Ketik 'stop' untuk keluar) ---")
        while True:
            try:
                msg = input() # Menunggu input user
                if msg.lower() == 'stop':
                    break
                
                # Pastikan sudah punya DES Key dan Public Key Teman
                if self.des_cipher and self.partner_rsa_public_pem:
                    # 1. Enkripsi Pesan (Confidentiality - DES)
                    padded = DES.add_padding(msg)
                    enc_hex = ""
                    for i in range(0, len(padded), 8):
                        enc_hex += self.des_cipher.encrypt_block(padded[i:i+8])
                    
                    # 2. Tanda Tangani Pesan Asli (Authentication - RSA Private Key Saya)
                    # Sesuai diagram: Source -> Encrypt(PRa)
                    signature = RSA.sign_message(msg, self.my_rsa_private)
                    
                    # 3. Format Paket: [DES_CIPHER] || [SIGNATURE]
                    payload_str = f"{enc_hex}||{signature}"
                    self.sock.sendall(HEADER_MSG + payload_str.encode('utf-8'))
                    
                    # Print konfirmasi di sisi sendiri
                    print(f"[Me] (Signed & Encrypted) -> {msg}")
                else:
                    print("[!] Tunggu koneksi stabil atau kunci belum lengkap...")
            except EOFError:
                break
            except KeyboardInterrupt:
                break

        self.sock.close()

    def receive_handler(self):
        """Thread yang menangani pesan masuk"""
        while True:
            try:
                data = self.sock.recv(4096)
                if not data: break

                # --- 1. Menerima Public Key Teman ---
                if data.startswith(HEADER_PUBKEY):
                    pub_pem = data[len(HEADER_PUBKEY):]
                    if pub_pem != self.my_rsa_public_pem:
                        self.partner_rsa_public_pem = pub_pem
                        print("\n[SYSTEM] Public Key Partner diterima.")
                        if self.is_host:
                            self.sock.sendall(HEADER_PUBKEY + self.my_rsa_public_pem)
                            if self.master_key_bytes:
                                print("[HOST] Mengenkripsi Kunci DES dengan Public Key Partner...")
                                enc_key = RSA.encrypt_secret_key(self.master_key_bytes, self.partner_rsa_public_pem)
                                self.sock.sendall(HEADER_SECRET + enc_key)
                                print("[HOST] Kunci DES Terenkripsi dikirim.")

                # --- 2. Menerima Kunci DES (Hanya Guest) ---
                elif data.startswith(HEADER_SECRET):
                    if not self.is_host and self.des_cipher is None:
                        try:
                            enc_bytes = data[len(HEADER_SECRET):]
                            key_bytes = RSA.decrypt_secret_key(enc_bytes, self.my_rsa_private)
                            hex_key = binascii.hexlify(key_bytes).decode('utf-8').upper()
                            self.des_cipher = DES.DES_Cipher(hex_key)
                            print(f"\n[GUEST] Kunci DES diterima & didekripsi: {hex_key}")
                            print("Siap Chatting!")
                        except Exception as e:
                            print(f"[ERROR] Gagal decrypt kunci DES: {e}")

                # --- 3. Menerima Pesan Chat (DES + Signature) ---
                elif data.startswith(HEADER_MSG):
                    if self.des_cipher:
                        payload = data[len(HEADER_MSG):].decode('utf-8')
                        try:
                            if '||' in payload:
                                enc_msg_hex, signature_hex = payload.split('||')
                                
                                # A. Dekripsi Pesan (Confidentiality)
                                dec_padded = ""
                                for i in range(0, len(enc_msg_hex), 16):
                                    dec_padded += self.des_cipher.decrypt_block(enc_msg_hex[i:i+16])
                                msg_content = DES.remove_padding(dec_padded)
                                
                                # B. Verifikasi Signature (Authentication)
                                # Pastikan partner_rsa_public_pem sudah ada
                                if self.partner_rsa_public_pem:
                                    is_valid = RSA.verify_signature(msg_content, signature_hex, self.partner_rsa_public_pem)
                                    valid_tag = "✅ VERIFIED" if is_valid else "❌ FAKE/CORRUPT"
                                else:
                                    valid_tag = "⚠️ UNKNOWN SENDER (No Key)"

                                print(f"\rTeman: {msg_content} [{valid_tag}]")
                                print("[Me] ", end="", flush=True)
                            else:
                                print("\r[!] Format pesan tidak valid (missing signature).")
                                
                        except ValueError:
                            print("\r[!] Format pesan rusak/padding error.")
                        except Exception as e:
                            print(f"\r[!] Error pemrosesan pesan: {e}")

            except Exception as e:
                # print(f"Error recv: {e}")
                break

if __name__ == "__main__":
    client = ChatClientFull()
    client.start()