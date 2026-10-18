# LeetCode #717: 1-bit and 2-bit Characters -- read from the start.
# Benchmark mirror of the Kara star arm: step past one bit on a 0 and
# two on a 1; the last character is one bit when a step lands on the
# last bit.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def is_one_bit_character(bits):
    n = len(bits)
    i = 0
    while i < n - 1:
        i += bits[i] + 1
    return i == n - 1


def main():
    seed = [717]
    strings = []
    for s in range(100):
        density = 1 + s % 3
        bits = [1 if next_random(seed) % 4 < density else 0 for _ in range(9999)]
        bits.append(0)
        strings.append(bits)
    yes = 0
    for rnd in range(400):
        for bits in strings:
            at = (rnd * 997) % 9999
            bits[at] = 1 - bits[at]
        for bits in strings:
            if is_one_bit_character(bits):
                yes += 1
    print(f"400 rounds of 100 strings of 10000 bits: {yes} one-bit endings")


main()
