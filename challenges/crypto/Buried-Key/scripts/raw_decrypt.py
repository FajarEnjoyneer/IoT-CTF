from Crypto.Cipher import AES
import binascii

key_hex = "5532a330d1e835e78b8188f8796bff06"
key = binascii.unhexlify(key_hex)
ciphertext_hex = "ba720d90a039d801adf22f86d2901b918f36fbbfa6459accb1c5315d1bd4cb39"
ciphertext = binascii.unhexlify(ciphertext_hex)

# Coba dekripsi langsung
cipher = AES.new(key, AES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)
print(plaintext)
