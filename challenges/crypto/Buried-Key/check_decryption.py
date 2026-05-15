from Crypto.Cipher import AES
import binascii

ciphertext_hex = "ba720d90a039d801adf22f86d2901b918f36fbbfa6459accb1c5315d1bd4cb39"
ciphertext = binascii.unhexlify(ciphertext_hex)

keys = ["e214b0df2caa60501d610087251b4f37", "5532a330d1e835e78b8188f8796bff06"]

for k_hex in keys:
    key = binascii.unhexlify(k_hex)
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(ciphertext)
    print(f"Key {k_hex}: {pt}")
