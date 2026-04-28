# CipherVeil — Secure Steganography Platform

[![CipherVeil Premium CI](https://github.com/Naveen-Veerapaneni/CipherVeil_Premium/actions/workflows/test.yml/badge.svg)](https://github.com/Naveen-Veerapaneni/CipherVeil_Premium/actions/workflows/test.yml)

> Invisible. Encrypted. Unbreakable.

A production-grade steganography web application that encrypts messages with **AES-256-GCM**, authenticates with **HMAC-SHA3-512**, and invisibly embeds them into images using **LSB Steganography**.

---

## ✨ Features

- 🔐 **AES-256-GCM** — authenticated encryption with random nonce per session
- 🛡️ **HMAC-SHA3-512** — independent 512-bit integrity verification
- 🖼️ **LSB Steganography** — bit-level embedding in pixel least-significant bits
- 🌙☀️ **Dark / Light Mode** — premium design in both themes
- 📱 **Responsive** — works on desktop and mobile
- 🔒 **Sensitive fields** hidden by default with toggle reveal
- 📋 **Copy-to-clipboard** with toast feedback

---

## 📁 Project Structure

```
CipherVeil/
├── app.py                    # Flask application & API routes
├── requirements.txt
├── encrypt/
│   ├── aes_gcm.py            # AES-256-GCM encrypt/decrypt
│   └── hmac_sha3.py          # HMAC-SHA3-512 generate/verify
├── steg/
│   ├── lsb_embed.py          # LSB bit embedding
│   └── lsb_extract.py        # LSB bit extraction
├── static/
│   ├── css/theme.css         # CSS custom properties (dark + light)
│   └── js/theme.js           # Theme toggle + persistence
└── templates/
    ├── index.html             # Home page + animated workflow
    ├── sender.html            # Sender module (3-step UI)
    └── receiver.html          # Receiver module (3-step UI)
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
http://localhost:5000
```

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/sender` | Sender module UI |
| GET | `/receiver` | Receiver module UI |
| POST | `/api/embed` | Encrypt + embed message into image |
| GET | `/api/download_stego` | Download the stego image |
| POST | `/api/extract` | Extract + verify + decrypt message |

### POST `/api/embed`
**Form data:** `image` (file), `message` (string)  
**Returns:** `ciphertext`, `nonce`, `tag`, `hmac`, `hmac_key`, `stego_image_b64`

### POST `/api/extract`
**Form data:** `image` (file), `hmac_key` (hex string), `tag` (hex, optional)  
**Returns:** `plaintext`, `ciphertext`, `nonce`, `tag`, `hmac`

---

## 🔒 Security Pipeline

```
Plaintext → AES-256-GCM → HMAC-SHA3-512 → LSB Embed → Stego Image
Stego Image → LSB Extract → HMAC Verify → AES-256-GCM Decrypt → Plaintext
```

---

## 🛠️ Requirements

- Python 3.9+
- Flask ≥ 3.0
- pycryptodome ≥ 3.20
- opencv-python-headless ≥ 4.9
- numpy ≥ 1.26
