def main():
    with open("challange/crypto/Buried-Key/buried_key", "rb") as f:
        f.seek(0xb7040)
        tbox10_raw = f.read(16 * 256)
    
    for i in range(16):
        table = tbox10_raw[i*256 : (i+1)*256]
        if len(set(table)) == 256:
            print(f"Tbox10 Table {i} is a permutation.")
        else:
            print(f"Tbox10 Table {i} is NOT a permutation! Unique values: {len(set(table))}")

if __name__ == "__main__":
    main()
