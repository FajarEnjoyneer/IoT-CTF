from Crypto.Cipher import AES

def main():
    with open("challange/crypto/Buried-Key/buried_key", "rb") as f:
        data = f.read()
    
    with open("challange/crypto/Buried-Key/buried_key", "rb") as f:
        f.seek(0xb6040)
        final_dec_raw = f.read(16 * 256)
    
    final_dec_inv = []
    for i in range(16):
        table = final_dec_raw[i*256 : (i+1)*256]
        inv = [0] * 256
        for x, v in enumerate(table): inv[v] = x
        final_dec_inv.append(inv)

    cipher_hex = "ba720d90a039d801adf22f86d2901b918f36fbbfa6459accb1c5315d1bd4cb39"
    cipher_bytes = bytes.fromhex(cipher_hex)
    std_cipher = bytes([final_dec_inv[i % 16][cipher_bytes[i]] for i in range(len(cipher_bytes))])

    # Try every 16-byte aligned and non-aligned sequence in the binary
    for i in range(0, len(data) - 16, 1):
        key = data[i:i+16]
        if all(b == 0 for b in key): continue
        
        aes = AES.new(key, AES.MODE_ECB)
        try:
            pt = aes.decrypt(std_cipher)
            if b"FLAG" in pt or b"flag" in pt:
                print(f"Found Key at offset {hex(i)}: {key.hex()}")
                print(f"Flag: {pt}")
                return
        except:
            continue

if __name__ == "__main__":
    main()
