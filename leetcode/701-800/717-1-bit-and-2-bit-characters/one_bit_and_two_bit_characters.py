# LeetCode #717: 1-bit and 2-bit Characters -- read from the start.
#
# A mirror of one_bit_and_two_bit_characters.kara (the ★ arm) and its
# harness.


def is_one_bit_character(bits):
    n = len(bits)
    i = 0
    while i < n - 1:
        i += bits[i] + 1
    return i == n - 1


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(bits):
    print(f"{bits} -> {'true' if is_one_bit_character(bits) else 'false'}")


def main():
    show([1, 0, 0])
    show([1, 1, 1, 0])
    show([0])
    show([1, 0])
    show([0, 0])
    show([1, 1, 0])
    show([0, 1, 0])
    show([1, 1, 1, 1, 0])
    show([0, 1, 1, 1, 0])
    odd = 0
    for n in range(1, 1001):
        if is_one_bit_character([1] * (n - 1) + [0]):
            odd += 1
    print(f"1 to 1000 bits, all ones but the last: {odd} one-bit endings")
    seed = [717]
    total = 0
    yes = 0
    for t in range(2000):
        n = 1 + next_random(seed) % 1000
        density = 1 + t % 3
        bits = [1 if next_random(seed) % 4 < density else 0 for _ in range(n - 1)]
        bits.append(0)
        answer = 1 if is_one_bit_character(bits) else 0
        yes += answer
        total = (total * 131 + answer + n) % 1000000007
    print(f"2000 random strings: {yes} one-bit endings, checksum {total}")


main()
