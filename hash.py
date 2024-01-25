from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode

class Hash:
    """Hash class for hashing and verifying passwords"""
    def derive_key_and_iv(password, length=32):
        """Derive a secret key and an IV from a given password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            #TODO add salt if needed
            salt=b'',  #! Empty salt
            iterations=100000,
            length=length * 2  # Double the length for both key and IV
        )
        key_iv = kdf.derive(password.encode())
        key, iv = key_iv[:length], key_iv[length:length+16]  # Assuming a 16-byte IV for AES
        return key, iv

    def encrypt(plaintext, password):
        """Encrypt plaintext using AES-256 CFB mode"""
        key, iv = Hash.derive_key_and_iv(password)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return urlsafe_b64encode(iv + ciphertext).decode('utf-8')

    def decrypt(ciphertext:str, password):
        """Decrypt ciphertext using AES-256 CFB mode"""
    
        data = urlsafe_b64decode(ciphertext)
    
        iv = data[:16]  # Extract the IV (16 bytes)

        ciphertext = data[16:]
    
        key, _ = Hash.derive_key_and_iv(password)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_text.decode()
