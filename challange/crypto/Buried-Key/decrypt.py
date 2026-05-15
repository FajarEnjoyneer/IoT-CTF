from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

key_hex = "5532a330d1e835e78b8188f8796bff06"
ciphertext_hex = "ba720d90a039d801adf22f86d2901b918f36fbbfa6459accb1c5315d1bd4cb39"

key = binascii.unhexlify(key_hex)
ciphertext = binascii.unhexlify(ciphertext_hex)

cipher = AES.new(key, AES.MODE_ECB)
padded_plaintext = cipher.decrypt(ciphertext)
plaintext = unpad(padded_plaintext, AES.block_size)

print(plaintext.decode('utf-8'))
