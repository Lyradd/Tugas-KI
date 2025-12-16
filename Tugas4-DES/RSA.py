import random
import math
import hashlib


def is_prime(n, k=5):
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
    while True:
        n = random.getrandbits(bits)
        if n % 2 == 0: n += 1
        if is_prime(n): return n

def mod_inverse(a, m):
    try:
        return pow(a, -1, m)
    except ValueError:
        return None 

# --- Fungsi Utama RSA ---

def generate_rsa_keypair(key_size=1024):
    """Menghasilkan pasangan kunci RSA."""
    print(f"Generating RSA primes (Please wait)...")
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
    
    private_key = (d, n)
    raw_public = f"{e}|{n}"
    public_key_pem_str = f"-----BEGIN PUBLIC KEY-----\n{raw_public}\n-----END PUBLIC KEY-----"
    
    return private_key, public_key_pem_str.encode('utf-8')

def encrypt_secret_key(secret_key_bytes, public_key_pem):
    """Enkripsi untuk Distribusi Kunci (Confidentiality): M^e mod n"""
    pem_str = public_key_pem.decode('utf-8')
    lines = pem_str.strip().split('\n')
    key_content = lines[1] 
    e_str, n_str = key_content.split('|')
    e, n = int(e_str), int(n_str)
    
    m_int = int.from_bytes(secret_key_bytes, byteorder='big')
    if m_int >= n: raise ValueError("Data too large for key size")
    
    c_int = pow(m_int, e, n)
    
    key_bytes_len = (n.bit_length() + 7) // 8
    return c_int.to_bytes(key_bytes_len, byteorder='big')

def decrypt_secret_key(encrypted_key_bytes, private_key):
    """Dekripsi untuk Distribusi Kunci: C^d mod n"""
    d, n = private_key
    c_int = int.from_bytes(encrypted_key_bytes, byteorder='big')
    m_int = pow(c_int, d, n)
    
    try:
        return m_int.to_bytes(8, byteorder='big') # Asumsi DES Key 8 byte
    except OverflowError:
        byte_len = (m_int.bit_length() + 7) // 8
        return m_int.to_bytes(byte_len, byteorder='big')

# --- DIGITAL SIGNATURE ---

def sign_message(message_str, private_key):
    """
    Membuat Tanda Tangan Digital.
    Proses: Hash(Pesan) -> Encrypt Hash pakai Private Key (Hash^d mod n)
    """
    d, n = private_key
    
    # 1. Buat Hash SHA-256 dari pesan
    msg_hash = hashlib.sha256(message_str.encode('utf-8')).hexdigest()
    msg_hash_int = int(msg_hash, 16)
    
    # 2. Sign: s = hash^d mod n
    signature_int = pow(msg_hash_int, d, n)
    
    # Return sebagai bytes hex string agar mudah dikirim
    sig_hex = hex(signature_int)[2:]
    return sig_hex

def verify_signature(message_str, signature_hex, public_key_pem):
    """
    Memverifikasi Tanda Tangan.
    Proses: Decrypt Signature pakai Public Key Sender -> Bandingkan dengan Hash(Pesan)
    """
    try:
        # Parsing Public Key Pengirim
        if isinstance(public_key_pem, bytes):
            public_key_pem = public_key_pem.decode('utf-8')
            
        lines = public_key_pem.strip().split('\n')
        key_content = lines[1]
        e_str, n_str = key_content.split('|')
        e, n = int(e_str), int(n_str)
        
        # 1. Dekripsi Signature: h' = s^e mod n
        signature_int = int(signature_hex, 16)
        decrypted_hash_int = pow(signature_int, e, n)
        decrypted_hash_hex = hex(decrypted_hash_int)[2:]
        
        # 2. Hitung Hash manual dari pesan yang diterima
        actual_hash = hashlib.sha256(message_str.encode('utf-8')).hexdigest()
        
        # Padding adjustment (kadang hex kehilangan leading zero)
        decrypted_hash_hex = decrypted_hash_hex.zfill(len(actual_hash))
        
        # 3. Bandingkan
        return decrypted_hash_hex == actual_hash
    except Exception as e:
        print(f"Verification Error: {e}")
        return False