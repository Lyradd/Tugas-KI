# client.py
import socket
import os
import binascii
import DES  # Mengimpor modul DES
import RSA  # Mengimpor modul RSA

def run_chat_client():
    TARGET_HOST = 'localhost' 
    TARGET_PORT = 5001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((TARGET_HOST, TARGET_PORT))
            print(f"Connected to server at {TARGET_HOST}:{TARGET_PORT}")
            
            # --- Tahap Pertukaran Kunci (Tidak Berubah) ---
            print("Receiving server's public key...")
            public_key_pem = b""
            while b"-----END PUBLIC KEY-----" not in public_key_pem:
                chunk = client_socket.recv(1024)
                if not chunk:
                    raise ConnectionError("Server disconnected during key exchange.")
                public_key_pem += chunk
            
            des_key_bytes = os.urandom(8)
            SECRET_KEY_HEX = binascii.hexlify(des_key_bytes).decode('utf-8').upper()
            print(f"Generated secret key: {SECRET_KEY_HEX}")
            
            print("Encrypting secret key...")
            encrypted_des_key = RSA.encrypt_secret_key(des_key_bytes, public_key_pem)
            
            print("Sending encrypted secret key to server...")
            client_socket.sendall(encrypted_des_key)
            
            cipher = DES.DES_Cipher(SECRET_KEY_HEX)
            print("DES Cipher object initialized with distributed key.")
            print("--- Sesi Chat Dimulai ---")
            
            # --- MODIFIKASI: Sesi Chat Looping ---
            while True:
                # 1. Client menerima pesan
                encrypted_message = client_socket.recv(1024).decode('utf-8')
                if not encrypted_message:
                    print("Server terputus.")
                    break
                
                decrypted_message_padded = ""
                for i in range(0, len(encrypted_message), 16):
                    hex_block = encrypted_message[i:i+16]
                    if len(hex_block) < 16:
                        continue
                    decrypted_message_padded += cipher.decrypt_block(hex_block)
                    
                final_message = DES.remove_padding(decrypted_message_padded)
                print(f"Server: {final_message}")

                # Periksa kondisi exit setelah menerima
                if final_message.lower() == 'stop':
                    print("Server menghentikan koneksi.")
                    break
                
                # 2. Client mengirim balasan
                message_to_send = input("Client: ")
                
                padded_message = DES.add_padding(message_to_send)
                encrypted_hex_response = ""
                for i in range(0, len(padded_message), 8):
                    block = padded_message[i:i+8]
                    encrypted_hex_response += cipher.encrypt_block(block)
                    
                client_socket.sendall(encrypted_hex_response.encode('utf-8'))

                # Periksa kondisi exit setelah mengirim
                if message_to_send.lower() == 'stop':
                    print("Klien menghentikan koneksi.")
                    break

        except ConnectionRefusedError:
            print(f"Koneksi ditolak. Apakah server sudah berjalan di {TARGET_HOST}:{TARGET_PORT}?")
        except ConnectionError as e:
            print(f"Koneksi error: {e}")
        except Exception as e:
            print(f"Terjadi error: {e}")
        finally:
            print("Koneksi ditutup.")

if __name__ == "__main__":
    run_chat_client()