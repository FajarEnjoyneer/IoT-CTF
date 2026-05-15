def main():
    with open("challange/crypto/Buried-Key/buried_key", "rb") as f:
        f.seek(0xb6040)
        final_dec_raw = f.read(16 * 256)
    
    final_dec_inv = []
    for i in range(16):
        table = final_dec_raw[i*256 : (i+1)*256]
        inv = [0] * 256
        for x, v in enumerate(table):
            inv[v] = x
        final_dec_inv.append(inv)
    
    # Example binary output for 00...00
    example_out_hex = "88f98d5e605eac3ee60fb40913896498"
    example_out_bytes = bytes.fromhex(example_out_hex)
    
    standard_out = []
    for i in range(16):
        standard_out.append(final_dec_inv[i][example_out_bytes[i]])
    
    print("Standard AES Output for 00...00:", bytes(standard_out).hex())

    # Challenge ciphertext
    challenge_out_hex = "ba720d90a039d801adf22f86d2901b918f36fbbfa6459accb1c5315d1bd4cb39"
    challenge_out_bytes = bytes.fromhex(challenge_out_hex)
    
    standard_challenge_out = []
    for j in range(len(challenge_out_bytes) // 16):
        block = challenge_out_bytes[j*16 : (j+1)*16]
        standard_block = []
        for i in range(16):
            standard_block.append(final_dec_inv[i][block[i]])
        standard_challenge_out.extend(standard_block)
    
    print("Standard Challenge Output:", bytes(standard_challenge_out).hex())

if __name__ == "__main__":
    main()
