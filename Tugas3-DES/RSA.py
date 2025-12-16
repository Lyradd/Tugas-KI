import random
import math

def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Menghasilkan bilangan prima acak dengan panjang bit tertentu."""
    while True:
        n = random.getrandbits(bits)
        if n % 2 == 0:
            n += 1
        if is_prime(n):
            return n

def mod_inverse(a, m):
    """Menghitung modular multiplicative inverse (d = e^-1 mod phi)."""
    try:
        return pow(a, -1, m)
    except ValueError:
        return None 

# --- Fungsi Utama RSA ---

def generate_rsa_keypair(key_size=1024):
    """
    Menghasilkan pasangan kunci privat dan publik secara manual.
    Catatan: key_size dikurangi defaultnya ke 1024 agar tidak terlalu lama di Python murni.
    """
    print(f"Generating primes")
    p = generate_prime(key_size // 2)
    q = generate_prime(key_size // 2)
    
    while p == q:
        q = generate_prime(key_size // 2)

    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    while math.gcd(e, phi) != 1:
        e = random.randrange(3, phi - 1, 2)

    d = mod_inverse(e, phi)
    
    # Format Kunci Privat: tuple (d, n)
    private_key = (d, n)
    
    raw_public = f"{e}|{n}"
    public_key_pem_str = f"-----BEGIN PUBLIC KEY-----\n{raw_public}\n-----END PUBLIC KEY-----"
    
    return private_key, public_key_pem_str.encode('utf-8')

def encrypt_secret_key(secret_key_bytes, public_key_pem):
    """
    Mengenkripsi bytes kunci rahasia menggunakan kunci publik (e, n).
    Algoritma: Cipher = Message^e mod n
    """
    # 1. Parsing Kunci Publik dari format "PEM" 
    pem_str = public_key_pem.decode('utf-8')
    lines = pem_str.strip().split('\n')
    key_content = lines[1] 
    e_str, n_str = key_content.split('|')
    e = int(e_str)
    n = int(n_str)
    
    # 2. Ubah pesan (bytes) menjadi integer (Message)
    m_int = int.from_bytes(secret_key_bytes, byteorder='big')
    
    if m_int >= n:
        raise ValueError("Pesan terlalu besar untuk ukuran kunci RSA ini.")
        
    # 3. Enkripsi: c = m^e mod n
    c_int = pow(m_int, e, n)
    
    # 4. Kembalikan sebagai bytes
    key_bytes_len = (n.bit_length() + 7) // 8
    encrypted_bytes = c_int.to_bytes(key_bytes_len, byteorder='big')
    
    return encrypted_bytes

def decrypt_secret_key(encrypted_key_bytes, private_key):
    """
    Mendekripsi bytes terenkripsi menggunakan kunci privat (d, n).
    Algoritma: Message = Cipher^d mod n
    """
    d, n = private_key
    
    # 1. Ubah cipher bytes menjadi integer
    c_int = int.from_bytes(encrypted_key_bytes, byteorder='big')
    
    # 2. Dekripsi: m = c^d mod n
    m_int = pow(c_int, d, n)
    
    # 3. Ubah kembali integer hasil dekripsi menjadi bytes
    try:
        decrypted_bytes = m_int.to_bytes(8, byteorder='big')
    except OverflowError:
        byte_len = (m_int.bit_length() + 7) // 8
        decrypted_bytes = m_int.to_bytes(byte_len, byteorder='big')
        
    return decrypted_bytes