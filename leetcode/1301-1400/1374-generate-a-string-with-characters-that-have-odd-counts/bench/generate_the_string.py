# LeetCode #1374 bench -- Python: the ★ arm: n a's when n is odd, and
# n - 1 a's and a b when it is even.


def generate_the_string(n):
    if n % 2 == 1:
        return "a" * n
    return "a" * (n - 1) + "b"


def main():
    # 10^7 rounds, each making the string for an n from 1 to 500,
    # drawn from the checksum so far, and reading its length and one
    # letter at a place drawn the same way
    check = 0
    for r in range(10000000):
        s = generate_the_string(1 + check % 500)
        b = ord(s[(check // 500) % len(s)])
        check = (check * 31 + len(s) + b + r) % 1000000007
    print(f"10000000 rounds: checksum {check}")


main()
