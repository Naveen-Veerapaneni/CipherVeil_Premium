"""
HMAC-SHA3-512 Authentication
Uses Python standard library only — no external dependencies.
"""
import hmac
import hashlib


def generate_hmac_sha3(data, key):
    return hmac.new(key, data, hashlib.sha3_512).hexdigest()


def verify_hmac_sha3(data, key, hmac_value):
    calc = hmac.new(key, data, hashlib.sha3_512).hexdigest()
    return hmac.compare_digest(calc, hmac_value)
