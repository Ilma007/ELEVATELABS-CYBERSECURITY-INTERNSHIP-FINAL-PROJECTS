# stego_tool.py
from PIL import Image
import os

# Optional encryption support
try:
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Random import get_random_bytes
    HAVE_CRYPTO = True
except Exception:
    HAVE_CRYPTO = False

MAGIC = b'STEG'  # 4 bytes

# -------- utilities --------
def bytes_to_bitstring(b: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in b)

def bitstring_to_bytes(s: str) -> bytes:
    return bytes(int(s[i:i+8], 2) for i in range(0, len(s), 8))

# -------- optional AES helpers (CBC PKCS7) --------
def derive_key(password: str, salt: bytes, key_len=32, iterations=100_000):
    if not HAVE_CRYPTO:
        raise RuntimeError("pycryptodome required for encryption")
    return PBKDF2(password.encode('utf-8'), salt, dkLen=key_len, count=iterations)

def pkcs7_pad(data: bytes, block_size=16):
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len])*pad_len

def pkcs7_unpad(data: bytes):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def encrypt_payload(payload: bytes, password: str) -> bytes:
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pkcs7_pad(payload))
    return salt + iv + ct

def decrypt_payload(enc: bytes, password: str) -> bytes:
    salt = enc[:16]
    iv = enc[16:32]
    ct = enc[32:]
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt_padded = cipher.decrypt(ct)
    return pkcs7_unpad(pt_padded)

# -------- header helpers --------
def build_header(filename: str, payload_bytes: bytes) -> bytes:
    fname_bytes = filename.encode('utf-8')
    payload_len = len(payload_bytes)
    header = MAGIC + payload_len.to_bytes(4, 'big') + len(fname_bytes).to_bytes(2, 'big') + fname_bytes
    return header

def parse_header(header_bytes: bytes):
    if len(header_bytes) < 10:
        raise ValueError("Header too short")
    if header_bytes[:4] != MAGIC:
        raise ValueError("Magic not found")
    payload_len = int.from_bytes(header_bytes[4:8], 'big')
    fname_len = int.from_bytes(header_bytes[8:10], 'big')
    return payload_len, fname_len

# -------- embedding --------
def embed_data_into_image(cover_path: str, out_path: str, payload_bytes: bytes, filename: str):
    img = Image.open(cover_path)
    # Use RGB/RGBA; convert to preserve channels
    img = img.convert('RGBA') if img.mode == 'RGBA' else img.convert('RGB')
    width, height = img.size
    channels = 4 if img.mode == 'RGBA' else 3
    capacity_bits = width * height * channels
    header = build_header(filename, payload_bytes)
    bitdata = bytes_to_bitstring(header + payload_bytes)
    if len(bitdata) > capacity_bits:
        raise ValueError(f"Not enough capacity: need {len(bitdata)} bits, have {capacity_bits} bits")
    pixels = list(img.getdata())
    new_pixels = []
    bit_idx = 0
    for px in pixels:
        px_list = list(px)
        for c in range(channels):
            if bit_idx < len(bitdata):
                px_list[c] = (px_list[c] & ~1) | int(bitdata[bit_idx])
                bit_idx += 1
        new_pixels.append(tuple(px_list))
    img_out = Image.new(img.mode, img.size)
    img_out.putdata(new_pixels)
    img_out.save(out_path)
    return out_path

# -------- extraction --------
def extract_data_from_image(stego_path: str):
    img = Image.open(stego_path)
    img = img.convert('RGBA') if img.mode == 'RGBA' else img.convert('RGB')
    channels = 4 if img.mode == 'RGBA' else 3
    pixels = list(img.getdata())

    # Read first 10 bytes (80 bits) for header
    bits = []
    needed_bits = 80
    i = 0
    while len(bits) < needed_bits and i < len(pixels):
        px = pixels[i]
        for c in range(channels):
            if len(bits) < needed_bits:
                bits.append(str(px[c] & 1))
        i += 1
    header_bytes = bitstring_to_bytes(''.join(bits))
    if header_bytes[:4] != MAGIC:
        raise ValueError("No stego header found")
    payload_len, fname_len = parse_header(header_bytes)
    extra_bytes_len = fname_len + payload_len
    extra_bits_needed = extra_bytes_len * 8

    # Now read full area (header + extra)
    collected = []
    total_needed = needed_bits + extra_bits_needed
    i = 0
    while len(collected) < total_needed and i < len(pixels):
        px = pixels[i]
        for c in range(channels):
            if len(collected) < total_needed:
                collected.append(str(px[c] & 1))
        i += 1
    if len(collected) < total_needed:
        raise ValueError("Image does not contain full payload")
    all_bits = ''.join(collected)
    extra_bits = all_bits[needed_bits:needed_bits + extra_bits_needed]
    extra_bytes = bitstring_to_bytes(extra_bits)
    fname_bytes = extra_bytes[:fname_len]
    payload_bytes = extra_bytes[fname_len:]
    filename = fname_bytes.decode('utf-8', errors='replace')
    return filename, payload_bytes

# -------- CLI helper functions --------
def embed_file_cli(cover_path, out_path, payload_path, password=None):
    with open(payload_path, 'rb') as f:
        payload = f.read()
    if password:
        if not HAVE_CRYPTO:
            raise RuntimeError("pycryptodome required to encrypt")
        payload = encrypt_payload(payload, password)
    filename = os.path.basename(payload_path)
    return embed_data_into_image(cover_path, out_path, payload, filename)

def extract_file_cli(stego_path, out_dir='.', password=None):
    filename, payload = extract_data_from_image(stego_path)
    if password:
        if not HAVE_CRYPTO:
            raise RuntimeError("pycryptodome required to decrypt")
        payload = decrypt_payload(payload, password)
    out_path = os.path.join(out_dir, filename)
    with open(out_path, 'wb') as f:
        f.write(payload)
    return out_path
