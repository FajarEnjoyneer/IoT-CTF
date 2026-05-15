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
    
    def get_standard(hex_str):
        b = bytes.fromhex(hex_str)
        return bytes([final_dec_inv[i][b[i]] for i in range(16)])

    correct = get_standard("88f98d5e605eac3ee60fb40913896498")
    faulty1 = get_standard("75f98d5e605eac2de60fc90913756498")
    faulty2 = get_standard("e6f98d5e605eacf9e60f850913076498")
    
    diff1 = bytes([correct[i] ^ faulty1[i] for i in range(16)])
    diff2 = bytes([correct[i] ^ faulty2[i] for i in range(16)])
    print(f"Diff 1: {diff1.hex()}")
    print(f"Diff 2: {diff2.hex()}")

if __name__ == "__main__":
    main()
