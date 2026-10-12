# Benchmark for #459: mirror of repeated_substring.kara (the star arm,
# every proper divisor) on the same workload.


def repeated_substring_pattern(s):
    cs = list(s)
    n = len(cs)
    for d in range(1, n // 2 + 1):
        if n % d != 0:
            continue
        repeats = True
        for i in range(d, n):
            if cs[i] != cs[i - d]:
                repeats = False
                break
        if repeats:
            return True
    return False


def main():
    strings = 10
    n = 100000
    rounds = 40
    units = [1, 5, 32, 100, 625, 1000, 3125, 5000, 20000, 50000]
    seed = 459

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    all_ = []
    for a in range(strings):
        unit = "".join(chr(97 + next_random() % 26) for _ in range(units[a]))
        all_.append(unit * (n // units[a]))
    found = 0
    checksum = 0
    for _ in range(rounds):
        for a in range(strings):
            hi = next_random()
            lo = next_random()
            k = n // 2 + (hi * 65536 + lo) % (n // 2)
            punch = next_random() % 2 == 0
            original = all_[a]
            if punch:
                cs = list(all_[a])
                cs[k] = chr(97 + (ord(cs[k]) - 97 + 1) % 26)
                all_[a] = "".join(cs)
            has = repeated_substring_pattern(all_[a])
            all_[a] = original
            if has:
                found += 1
            checksum = (checksum * 31 + (units[a] if has else k)) % 1000000007
    print(f"{rounds} rounds on {strings} strings of {n}: {found} repeat a substring, checksum {checksum}")


main()
