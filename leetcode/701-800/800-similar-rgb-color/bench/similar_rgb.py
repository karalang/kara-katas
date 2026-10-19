# LeetCode 800 -- Similar RGB Color: the bench, in Python. Mirrors
# similar_rgb.kara: each part rounded to the nearest doubled digit.
seed = 800
DIGITS = "0123456789abcdef"


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digit(c):
    return c - 48 if 48 <= c <= 57 else c - 97 + 10


def similar_rgb(color):
    b = color.encode()
    out = "#"
    for p in range(3):
        part = digit(b[1 + 2 * p]) * 16 + digit(b[2 + 2 * p])
        d = DIGITS[(part + 8) // 17]
        out += d + d
    return out


def main():
    colors = ["#" + "".join(DIGITS[next_random() % 16] for _ in range(6)) for _ in range(4096)]
    rounds = 40960000
    check = 0
    for r in range(rounds):
        got = similar_rgb(colors[r % 4096]).encode()
        check = (check * 31 + got[1] * 65536 + got[3] * 256 + got[5]) % 1000000007
    print(f"{rounds} colours: checksum {check}")


main()
