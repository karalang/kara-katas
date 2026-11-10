# LeetCode #2075: Decode the Slanted Ciphertext -- Python mirror of the ★
# arm (slanted.kara): the grid's diagonals read from left to right, the
# trailing spaces trimmed.


def decode_ciphertext(encoded_text, rows):
    cols = len(encoded_text) // rows
    plain = []
    for c in range(cols):
        r = 0
        while r < rows and c + r < cols:
            plain.append(encoded_text[r * cols + c + r])
            r += 1
    return "".join(plain).rstrip(" ")


seed = 2075


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(rows, cols, alphabet):
    return "".join(alphabet[next_random() % len(alphabet)] for _ in range(rows * cols))


def checksum(s):
    check = 0
    for b in s.encode():
        check = (check * 31 + b) % 1000000007
    return check


def main():
    examples = [
        ("ch   ie   pr", 3),
        ("iveo    eed   l te   olc", 4),
        ("coding", 1),
        (" b  ac", 2),
        ("", 5),
        ("a  b  c ", 2),
        ("abcd", 4),
    ]
    for text, rows in examples:
        print(f'"{text}", rows = {rows} -> "{decode_ciphertext(text, rows)}"')
    total = 0
    check = 0
    for _ in range(400):
        rows = next_random() % 8 + 1
        cols = next_random() % 31
        alphabet = ["ab ", "abcdefgh  ", "    x"][next_random() % 3]
        text = random_text(rows, cols, alphabet)
        plain = decode_ciphertext(text, rows)
        total += len(plain)
        check = (check * 31 + checksum(plain)) % 1000000007
    print(f"400 grids: {total} characters, checksum {check}")
    text = random_text(1000, 1000, "abcdefghijklmnopqrstuvwxyz     ")
    plain = decode_ciphertext(text, 1000)
    print(f"1000 rows of 1000: {len(plain)} characters, checksum {checksum(plain)}")


main()
