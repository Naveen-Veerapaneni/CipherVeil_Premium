import cv2
import numpy as np


def embed_data(image_path, data_bytes, output_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Cover image not found.")

    img = img.astype(np.uint8)
    flat = img.flatten()

    data_bits = np.unpackbits(np.frombuffer(data_bytes, dtype=np.uint8))
    total_bits = len(data_bits)

    if total_bits > len(flat):
        raise ValueError(f"Payload too large: {total_bits} bits, capacity = {len(flat)} bits")

    flat = flat.astype(np.uint8)

    for i in range(total_bits):
        flat[i] = (flat[i] & 0xFE) | data_bits[i]

    stego = flat.reshape(img.shape)
    cv2.imwrite(output_path, stego)
