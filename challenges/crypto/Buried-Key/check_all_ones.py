from Crypto.Cipher import AES
import binascii

input_hex = "ffffffffffffffffffffffffffffffff"
pt = binascii.unhexlify(input_hex)

keys = ["e214b0df2caa60501d610087251b4f37", "5532a330d1e835e78b8188f8796bff06"]

for k_hex in keys:
    key = binascii.unhexlify(k_hex)
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pt)
    print(f"Key {k_hex}: {binascii.hexlify(ct).decode()}")
