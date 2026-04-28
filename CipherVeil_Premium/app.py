import os
import io
import base64
import tempfile
from flask import Flask, render_template, request, jsonify, send_file

from encrypt.aes_gcm import aes_gcm_encrypt, aes_gcm_decrypt
from encrypt.hmac_sha3 import generate_hmac_sha3, verify_hmac_sha3
from steg.lsb_embed import embed_data
from steg.lsb_extract import extract_data

app = Flask(__name__)
app.secret_key = os.urandom(32)

# Shared keys (in production these would be securely managed)
AES_KEY = b"1234567890abcdef1234567890abcdef"
SECRET_HMAC_KEY = b"fedcba0987654321fedcba0987654321"

UPLOAD_FOLDER = tempfile.gettempdir()


# ─────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sender")
def sender():
    return render_template("sender.html")


@app.route("/receiver")
def receiver():
    return render_template("receiver.html")


# ─────────────────────────────────────────
#  SENDER API
# ─────────────────────────────────────────

@app.route("/api/embed", methods=["POST"])
def api_embed():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files["image"]
        message = request.form.get("message", "").strip()

        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Save uploaded image to temp
        ext = os.path.splitext(image_file.filename)[1].lower() or ".png"
        input_path = os.path.join(UPLOAD_FOLDER, f"cover{ext}")
        image_file.save(input_path)

        # AES-GCM Encrypt
        ciphertext, nonce, tag = aes_gcm_encrypt(message, AES_KEY)

        # HMAC-SHA3-512 over combined payload
        combined = ciphertext + nonce + tag
        hmac_value = generate_hmac_sha3(combined, SECRET_HMAC_KEY)

        # Build payload: [2-byte len][ciphertext][nonce 16B][tag 16B][hmac 64B]
        payload = (
            len(ciphertext).to_bytes(2, "big") +
            ciphertext +
            nonce +
            tag +
            bytes.fromhex(hmac_value)
        )

        # Embed into image
        output_path = os.path.join(UPLOAD_FOLDER, "stego_output.png")
        embed_data(input_path, payload, output_path)

        # Read stego image and base64-encode for preview
        with open(output_path, "rb") as f:
            stego_b64 = base64.b64encode(f.read()).decode()

        return jsonify({
            "success": True,
            "ciphertext": ciphertext.hex(),
            "nonce": nonce.hex(),
            "tag": tag.hex(),
            "hmac": hmac_value,
            "hmac_key": SECRET_HMAC_KEY.hex(),
            "stego_image_b64": stego_b64,
            "payload_bytes": len(payload)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/download_stego")
def download_stego():
    path = os.path.join(UPLOAD_FOLDER, "stego_output.png")
    if not os.path.exists(path):
        return jsonify({"error": "No stego image found"}), 404
    return send_file(path, as_attachment=True, download_name="stego_secure.png")


# ─────────────────────────────────────────
#  RECEIVER API
# ─────────────────────────────────────────

@app.route("/api/extract", methods=["POST"])
def api_extract():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No stego image uploaded"}), 400

        stego_file = request.files["image"]
        hmac_key_hex = request.form.get("hmac_key", "").strip()
        input_tag_hex = request.form.get("tag", "").strip()

        # Save stego image
        stego_path = os.path.join(UPLOAD_FOLDER, "stego_input.png")
        stego_file.save(stego_path)

        # Extract header to get ciphertext length
        header = extract_data(stego_path, 2)
        cipher_len = int.from_bytes(header, "big")
        total = 2 + cipher_len + 16 + 16 + 64

        payload = extract_data(stego_path, total)

        idx = 0
        c_len = int.from_bytes(payload[idx:idx+2], "big")
        idx += 2

        ciphertext = payload[idx:idx+c_len]
        idx += c_len

        nonce = payload[idx:idx+16]
        idx += 16

        tag = payload[idx:idx+16]
        idx += 16

        extracted_hmac = payload[idx:idx+64].hex()

        # Verify HMAC
        try:
            user_key = bytes.fromhex(hmac_key_hex)
        except Exception:
            return jsonify({"error": "Invalid HMAC key format (must be hex)"}), 400

        combined = ciphertext + nonce + tag
        computed_hmac = generate_hmac_sha3(combined, user_key)

        if computed_hmac != extracted_hmac:
            return jsonify({"error": "HMAC verification FAILED — message may be tampered!"}), 400

        # Verify TAG
        if input_tag_hex and input_tag_hex != tag.hex():
            return jsonify({"error": "AES-GCM TAG mismatch — data integrity check failed!"}), 400

        # Decrypt
        plaintext = aes_gcm_decrypt(ciphertext, AES_KEY, nonce, tag)

        return jsonify({
            "success": True,
            "plaintext": plaintext,
            "ciphertext": ciphertext.hex(),
            "nonce": nonce.hex(),
            "tag": tag.hex(),
            "hmac": extracted_hmac,
            "hmac_verified": True
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Decryption error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
