def get_sbox():
    return [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]

def galois_mul(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a <<= 1
        if hi:
            a ^= 0x1b
        a &= 0xff
        b >>= 1
    return p

def solve_column(correct, faulty_list, indices):
    sbox = get_sbox()
    candidates = set(range(256**4)) # Too large to iterate directly.
    # Instead, let's iterate over K10 candidates for each byte and check consistency.
    
    # K10 candidate for indices[0], indices[1], indices[2], indices[3]
    possible_k10 = []
    for _ in range(4):
        possible_k10.append(set(range(256)))

    # For each faulty ciphertext
    for faulty in faulty_list:
        new_possible = [set() for _ in range(4)]
        # The fault was a single byte delta before MixColumns.
        # MC output diff is (2*delta, delta, delta, 3*delta) - or permutation.
        # But we don't know the order. Standard AES MC:
        # [2 3 1 1]   [delta]   [2*delta]
        # [1 2 3 1] * [0    ] = [delta  ]
        # [1 1 2 3]   [0    ]   [delta  ]
        # [3 1 1 2]   [0    ]   [3*delta]
        # Indices after ShiftRows: 0, 13, 10, 7 for Col 0.
        # They correspond to Row 0, 1, 2, 3 of the column.
        
        for delta in range(1, 256):
            diffs_expected = [galois_mul(2, delta), delta, delta, galois_mul(3, delta)]
            
            # Try matching these expected diffs to our indices
            # indices = [i0, i1, i2, i3]
            # correct[i0] ^ faulty[i0] = Sbox(X0) ^ Sbox(X0 ^ diffs_expected[0])
            
            for k0 in range(256):
                x0 = sbox.index(correct[indices[0]] ^ k0)
                if (sbox[x0] ^ sbox[x0 ^ diffs_expected[0]]) == (correct[indices[0]] ^ faulty[indices[0]]):
                    for k1 in range(256):
                        x1 = sbox.index(correct[indices[1]] ^ k1)
                        if (sbox[x1] ^ sbox[x1 ^ diffs_expected[1]]) == (correct[indices[1]] ^ faulty[indices[1]]):
                             # ... this is still slow.
                             pass

    # Let's use a simpler approach. For each byte i, and each delta, find possible k_i.
    # Then combine.
    
    final_k10 = [None] * 16
    
    return None

# Rewriting solver to be more efficient
def solve_k10():
    sbox = get_sbox()
    
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
    
    faults = [
        ["75f98d5e605eac2de60fc90913756498", "e6f98d5e605eacf9e60f850913076498"], # Col 0
        ["88f98daf605edf3ee651b40997896498", "88f98d3e605ea73ee6c6b4096f896498"], # Col 1
        ["88f9015e6046ac3e300fb409138964f8", "88f93c5e604aac3e250fb40913896494"], # Col 2
        ["88748d5e295eac3ee60fb48d13897a98", "88278d5ef15eac3ee60fb49013892d98"]  # Col 3
    ]
    
    col_indices = [
        [0, 13, 10, 7],
        [4, 1, 14, 11],
        [8, 5, 2, 15],
        [12, 9, 6, 3]
    ]
    
    k10 = [0] * 16
    
    for col in range(4):
        indices = col_indices[col]
        f1 = get_standard(faults[col][0])
        f2 = get_standard(faults[col][1])
        
        candidates = []
        # Iterating over all 4 bytes of K10 for this column
        # But we can do it byte by byte for each delta.
        possible_k_for_col = None
        
        for f_bytes in [f1, f2]:
            current_f_possible = set()
            for delta in range(1, 256):
                diffs_exp = [galois_mul(2, delta), delta, delta, galois_mul(3, delta)]
                
                col_k_cands = [[] for _ in range(4)]
                for i in range(4):
                    idx = indices[i]
                    diff_actual = correct[idx] ^ f_bytes[idx]
                    for k in range(256):
                        x = sbox.index(correct[idx] ^ k)
                        if sbox[x] ^ sbox[x ^ diffs_exp[i]] == diff_actual:
                            col_k_cands[i].append(k)
                
                if all(col_k_cands):
                    import itertools
                    for combo in itertools.product(*col_k_cands):
                        current_f_possible.add(combo)
            
            if possible_k_for_col is None:
                possible_k_for_col = current_f_possible
            else:
                possible_k_for_col &= current_f_possible
        
        if len(possible_k_for_col) == 1:
            res = list(possible_k_for_col)[0]
            for i in range(4):
                k10[indices[i]] = res[i]
            print(f"Column {col} K10: {res}")
        else:
            print(f"Column {col} candidates: {len(possible_k_for_col)}")
            if possible_k_for_col:
                res = list(possible_k_for_col)[0]
                for i in range(4):
                    k10[indices[i]] = res[i]

    print(f"Full K10: {bytes(k10).hex()}")

if __name__ == "__main__":
    solve_k10()
