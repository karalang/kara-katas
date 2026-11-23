# LeetCode #2525: Categorize Box According to Criteria -- Python mirror of
# the ★ arm (flags.kara): two flags, then a match on the pair.


def categorize_box(length, width, height, mass):
    bulky = length >= 10000 or width >= 10000 or height >= 10000 or length * width * height >= 1000000000
    heavy = mass >= 100
    match (bulky, heavy):
        case (True, True):
            return "Both"
        case (True, False):
            return "Bulky"
        case (False, True):
            return "Heavy"
        case _:
            return "Neither"


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def wide_random(seed):
    return next_random(seed) * 32768 + next_random(seed)


def main():
    fixed = [
        (1000, 35, 700, 300),
        (200, 50, 800, 50),
        (10000, 1, 1, 1),
        (9999, 1, 1, 100),
        (1000, 1000, 1000, 100),
        (999, 1000, 1000, 99),
        (100000, 100000, 100000, 1000),
        (1, 1, 1, 1),
        (1, 9999, 9999, 99),
        (2, 9999, 9999, 100),
    ]
    for length, width, height, mass in fixed:
        print(f"{length} {width} {height} {mass} -> {categorize_box(length, width, height, mass)}")
    seed = [2525]
    for top in [100000, 2000]:
        counts = [0, 0, 0, 0]
        for _ in range(100000):
            length = wide_random(seed) % top + 1
            width = wide_random(seed) % top + 1
            height = wide_random(seed) % top + 1
            mass = next_random(seed) % 1000 + 1
            name = categorize_box(length, width, height, mass)
            at = 0 if name == "Both" else 1 if name == "Bulky" else 2 if name == "Heavy" else 3
            counts[at] += 1
        print(f"10^5 random to {top}: Both {counts[0]}, Bulky {counts[1]}, Heavy {counts[2]}, Neither {counts[3]}")


main()
