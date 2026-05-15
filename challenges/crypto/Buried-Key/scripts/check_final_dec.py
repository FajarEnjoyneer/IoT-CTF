def main():
    with open("challange/crypto/Buried-Key/buried_key", "rb") as f:
        f.seek(0xb6040)
        final_dec_raw = f.read(16 * 256)
    
    for i in range(16):
        table = final_dec_raw[i*256 : (i+1)*256]
        if len(set(table)) == 256:
            print(f"Table {i} is a permutation.")
        else:
            print(f"Table {i} is NOT a permutation! Unique values: {len(set(table))}")

if __name__ == "__main__":
    main()
