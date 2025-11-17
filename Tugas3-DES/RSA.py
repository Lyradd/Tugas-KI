# RSA.py
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_rsa_keypair():
    """Menghasilkan pasangan kunci privat dan kunci publik (PEM format)."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    
    # Serialisasi kunci publik untuk dikirim
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_key, public_key_pem

def encrypt_secret_key(secret_key_bytes, public_key_pem):
    """Mengenkripsi kunci rahasia (bytes) menggunakan kunci publik PEM."""
    # Load kunci publik dari format PEM
    public_key = serialization.load_pem_public_key(public_key_pem)
    
    encrypted_key = public_key.encrypt(
        secret_key_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

def decrypt_secret_key(encrypted_key_bytes, private_key):
    """Mendekripsi kunci rahasia terenkripsi menggunakan kunci privat."""
    decrypted_key = private_key.decrypt(
        encrypted_key_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key