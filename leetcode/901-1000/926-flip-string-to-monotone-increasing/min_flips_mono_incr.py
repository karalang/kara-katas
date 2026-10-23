# LeetCode #926: Flip String to Monotone Increasing -- one pass (Python mirror).


def min_flips_mono_incr(s):
    flips = 0
    ones = 0
    for c in s:
        if c == "1":
            ones += 1
        else:
            flips = min(flips + 1, ones)
    return flips


seed = 926


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}": {min_flips_mono_incr(s)}')


def random_string(n, lean):
    return "".join("1" if next_random() % 100 < lean else "0" for _ in range(n))


def main():
    for s in ["00110", "010110", "00011000", "0", "1", "0011", "10", "11100", "1010101", "0101010"]:
        show(s)
    total = 0
    check = 0
    for r in range(300):
        n = 1 + next_random() % 2000
        lean = r % 101
        a = min_flips_mono_incr(random_string(n, lean))
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"300 random strings: answers summing to {total}, checksum {check}")
    back = "1" * 50000 + "0" * 50000
    alt = "01" * 50000
    r = random_string(100000, 50)
    print(f"100000 characters: 1s then 0s {min_flips_mono_incr(back)}, alternating {min_flips_mono_incr(alt)}, random {min_flips_mono_incr(r)}")


main()
