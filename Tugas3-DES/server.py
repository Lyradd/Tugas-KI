# server.py
import socket
import binascii
import DES  # Mengimpor modul DES
import RSA  # Mengimpor modul RSA

def run_chat_server():
    HOST_ADDRESS = '0.0.0.0'  
    PORT_NUMBER = 5001
    
    print("Generating RSA key pair (2048 bit)...")
    private_key, public_key_pem = RSA.generate_rsa_keypair()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST_ADDRESS, PORT_NUMBER))
        server_socket.listen(1)
        print(f"Chat Server listening on {HOST_ADDRESS}:{PORT_NUMBER}...")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connection established with {addr}")
            try:
                # --- Tahap Pertukaran Kunci (Tidak Berubah) ---
                print("Sending public key to client...")
                conn.sendall(public_key_pem)
                
                print("Waiting for encrypted secret key...")
                encrypted_des_key = conn.recv(256) 
                if not encrypted_des_key:
                    raise ConnectionError("Client disconnected during key exchange.")

                print("Decrypting secret key...")
                des_key_bytes = RSA.decrypt_secret_key(encrypted_des_key, private_key)
                
                SECRET_KEY_HEX = binascii.hexlify(des_key_bytes).decode('utf-8').upper()
                print(f"Successfully decrypted secret key: {SECRET_KEY_HEX}")

                cipher = DES.DES_Cipher(SECRET_KEY_HEX)
                print("DES Cipher object initialized with distributed key.")
                print("--- Sesi Chat Dimulai ---")

                # --- MODIFIKASI: Sesi Chat Looping ---
                while True:
                    # 1. Server mengirim pesan
                    message_to_send = input("Server: ")
                    
                    padded_message = DES.add_padding(message_to_send)
                    encrypted_hex_output = ""
                    for i in range(0, len(padded_message), 8):
                        block = padded_message[i:i+8]
                        encrypted_hex_output += cipher.encrypt_block(block)
                        
                    conn.sendall(encrypted_hex_output.encode('utf-8'))

                    # Periksa kondisi exit setelah mengirim
                    if message_to_send.lower() == 'stop':
                        print("Server menghentikan koneksi.")
                        break
                    
                    # 2. Server menerima balasan
                    encrypted_response = conn.recv(1024).decode('utf-8')
                    if not encrypted_response:
                        print("Klien terputus.")
                        break
                    
                    decrypted_response_padded = ""
                    for i in range(0, len(encrypted_response), 16):
                        hex_block = encrypted_response[i:i+16]
                        decrypted_response_padded += cipher.decrypt_block(hex_block)
                        
                    final_response = DES.remove_padding(decrypted_response_padded)
                    print(f"Client: {final_response}")

                    # Periksa kondisi exit setelah menerima
                    if final_response.lower() == 'stop':
                        print("Klien menghentikan koneksi.")
                        break
                
            except ConnectionError as e:
                print(f"Koneksi error: {e}")
            except Exception as e:
                print(f"Terjadi error: {e}")
            finally:
                print("Koneksi ditutup.")

if __name__ == "__main__":
    run_chat_server()