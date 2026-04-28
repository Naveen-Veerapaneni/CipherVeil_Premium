import cv2
import numpy as np


def extract_data(stego_path, payload_size):
    img = cv2.imread(stego_path)

    if img is None:
        raise ValueError("Stego image not found.")

    img = img.astype(np.uint8)
    flat = img.flatten()

    num_bits = payload_size * 8
    bits = [(flat[i] & 1) for i in range(num_bits)]

    return np.packbits(bits).tobytes()
