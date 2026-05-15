from Crypto.Cipher import AES
import binascii

key = binascii.unhexlify("5532a330d1e835e78b8188f8796bff06")
ciphertext = binascii.fromhex("ba720d90a039d801adf22f86d2901b918f36fbbfa6459accb1c5315d1bd4cb39")

# FinalDec inversion
with open("challange/crypto/Buried-Key/buried_key", "rb") as f:
    f.seek(0xb6040)
    final_dec_raw = f.read(16 * 256)

final_dec_inv = []
for i in range(16):
    table = final_dec_raw[i*256 : (i+1)*256]
    inv = [0] * 256
    for x, v in enumerate(table): inv[v] = x
    final_dec_inv.append(inv)

# Apply FinalDec_inv on the whole ciphertext
std_cipher = bytes([final_dec_inv[i % 16][ciphertext[i]] for i in range(len(ciphertext))])

# Decrypt
aes = AES.new(key, AES.MODE_ECB)
pt = aes.decrypt(std_cipher)
print(pt)
