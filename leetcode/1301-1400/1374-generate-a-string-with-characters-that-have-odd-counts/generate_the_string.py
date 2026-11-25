# LeetCode #1374: Generate a String With Characters That Have Odd Counts
# -- Python mirror of the ★ arm: n a's when n is odd, and n - 1 a's and a
# b when it is even.


def generate_the_string(n):
    if n % 2 == 1:
        return "a" * n
    return "a" * (n - 1) + "b"


def main():
    print(" ".join(generate_the_string(n) for n in [4, 2, 7]))
    letters = 0
    bs = 0
    check = 0
    for n in range(1, 501):
        s = generate_the_string(n)
        letters += len(s)
        for b in s.encode():
            if b == ord("b"):
                bs += 1
            check = (check * 131 + b) % 1000000007
    print(f"n from 1 to 500: {letters} letters, {bs} b's, checksum {check}")


main()
