import socket
import threading

clients = []

def broadcast(message, sender_socket):
    """Mengirim pesan ke semua client KECUALI pengirim."""
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except:
                # Jika pengiriman gagal, anggap client putus
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket, addr):
    """Menangani komunikasi satu client."""
    print(f"[INFO] Koneksi baru dari {addr}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(4096)
            if not message:
                break
            print(f"[RELAY] Menerima {len(message)} bytes data terenkripsi dari {addr}")
            print(f"        Cuplikan (Hex): {message[:20].hex().upper()}...") 
            
            # Teruskan ke semua client lain apa adanya
            broadcast(message, client_socket)
            
    except Exception as e:
        print(f"[ERROR] {addr} terputus: {e}")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
        print(f"[INFO] Koneksi {addr} ditutup.")

def run_server():
    HOST = '0.0.0.0'
    PORT = 5001
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print("="*40)
    print(f"BLIND RELAY SERVER berjalan di {HOST}:{PORT}")
    print("Server ini TIDAK memiliki kunci dekripsi.")
    print("Server hanya meneruskan ciphertext.")
    print("="*40)
    
    try:
        while True:
            client_sock, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_sock, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\nServer berhenti.")
    finally:
        server.close()

if __name__ == "__main__":
    run_server()