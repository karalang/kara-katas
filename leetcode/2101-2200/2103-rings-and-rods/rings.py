# LeetCode #2103: Rings and Rods -- Python mirror of the ★ arm
# (rings.kara): a mask per rod, red 1, green 2 and blue 4, and the rods
# whose mask is 7 counted. Prints the same lines.


def count_points(rings):
    b = rings.encode()
    masks = [0] * 10
    i = 0
    while i < len(b):
        c = b[i]
        bit = 1 if c == ord("R") else 2 if c == ord("G") else 4
        masks[b[i + 1] - ord("0")] |= bit
        i += 2
    return sum(1 for m in masks if m == 7)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    every = "".join(f"R{d}G{d}B{d}" for d in range(10))
    examples = [
        "B0B6G0R6R0R6G9",
        "B0R0G0R9R0B0G0",
        "G4",
        every,
        "R3R3R3R3",
        "R1G1R2G2",
        "R0G1B2" * 33 + "R0",
    ]
    for rings in examples:
        print(f"{rings} -> {count_points(rings)}")
    seed = [2103]
    total = 0
    check = 0
    for rnd in range(3000):
        n = next_random(seed) % 100 + 1
        rods = 10 if rnd % 2 == 0 else 3
        parts = []
        for _ in range(n):
            parts.append("RGB"[next_random(seed) % 3])
            parts.append(chr(ord("0") + next_random(seed) % rods))
        got = count_points("".join(parts))
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"3000 strings: {total} rods with all three, checksum {check}")


main()
