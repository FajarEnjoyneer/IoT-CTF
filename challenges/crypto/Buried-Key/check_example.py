from Crypto.Cipher import AES
import binascii

key_hex = "5532a330d1e835e78b8188f8796bff06"
input_hex = "00000000000000000000000000000000"

key = binascii.unhexlify(key_hex)
plaintext = binascii.unhexlify(input_hex)

cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(plaintext)

print(f"Standard AES: {binascii.hexlify(ciphertext).decode()}")
