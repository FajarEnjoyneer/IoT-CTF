from Crypto.Cipher import AES
import binascii

key = binascii.unhexlify("5532a330d1e835e78b8188f8796bff06")
aes = AES.new(key, AES.MODE_ECB)
std_pt = aes.encrypt(bytes([0]*16))

binary_out = bytes.fromhex("88f98d5e605eac3ee60fb40913896498")

# Temukan pemetaan FinalDec byte-demi-byte
mapping = [{} for _ in range(16)]
for i in range(16):
    mapping[i][std_pt[i]] = binary_out[i]

print(mapping)
