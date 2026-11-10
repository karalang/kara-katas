# LeetCode #2075: Decode the Slanted Ciphertext -- Python mirror of the ★
# arm's benchmark (slanted.kara): 40 grids of 10^6 characters in 1 to 1000
# rows, built once and decoded.


def decode_ciphertext(encoded_text, rows):
    cols = len(encoded_text) // rows
    plain = []
    for c in range(cols):
        r = 0
        while r < rows and c + r < cols:
            plain.append(encoded_text[r * cols + c + r])
            r += 1
    return "".join(plain).rstrip(" ")


def main():
    letters = "abcdefghijklmnopqrstuvwxyz      "
    seed = 2075
    grids = []
    for g in range(40):
        rows = [1, 2, 10, 100, 1000][g % 5]
        chars = []
        for _ in range(1000000 // rows * rows):
            seed = (seed * 1103515245 + 12345) % 2147483648
            chars.append(letters[(seed // 65536) % 32])
        grids.append(("".join(chars), rows))
    total = 0
    check = 0
    for text, rows in grids:
        plain = decode_ciphertext(text, rows)
        total += len(plain)
        for b in plain.encode():
            check = (check * 31 + b) % 1000000007
    print(f"40 grids: {total} characters, checksum {check}")


main()
