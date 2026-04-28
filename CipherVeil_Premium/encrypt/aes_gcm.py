"""
AES-256-GCM Authenticated Encryption
Compatible with pycryptodome OR the cryptography library.
"""
import os

try:
    from Crypto.Cipher import AES as _AES

    def aes_gcm_encrypt(message, key):
        cipher = _AES.new(key, _AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        return ciphertext, cipher.nonce, tag

    def aes_gcm_decrypt(ciphertext, key, nonce, tag):
        cipher = _AES.new(key, _AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

except ImportError:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    def aes_gcm_encrypt(message, key):
        nonce = os.urandom(16)
        aesgcm = AESGCM(key)
        ct_with_tag = aesgcm.encrypt(nonce, message.encode(), None)
        ciphertext = ct_with_tag[:-16]
        tag = ct_with_tag[-16:]
        return ciphertext, nonce, tag

    def aes_gcm_decrypt(ciphertext, key, nonce, tag):
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext + tag, None)
        return plaintext.decode()
