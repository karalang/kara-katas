# Benchmark for #567: Python mirror of the ★ arm (a sliding window); see
# check_inclusion.kara.


def check_inclusion(s1, s2):
    a = list(s1)
    b = list(s2)
    k = len(a)
    if k > len(b):
        return False
    need = [0] * 26
    for c in a:
        need[ord(c) - ord("a")] += 1
    missing = k
    for i in range(len(b)):
        enter = ord(b[i]) - ord("a")
        if need[enter] > 0:
            missing -= 1
        need[enter] -= 1
        if i >= k:
            leave = ord(b[i - k]) - ord("a")
            need[leave] += 1
            if need[leave] > 0:
                missing += 1
        if missing == 0:
            return True
    return False


# ---- benchmark --------------------------------------------------------------

seed = 567


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(length, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(alphabet[step() % letters] for _ in range(length))


def main():
    count = 100
    rounds = 300
    pairs = []
    for g in range(count):
        letters = 3 + step() % 24
        s1 = random_text(5 + step() % 196, letters)
        s2 = random_text(10000, letters)
        if g % 2 == 0:
            shuffled = list(s1)
            i = len(shuffled) - 1
            while i > 0:
                j = step() % (i + 1)
                shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
                i -= 1
            cut = step() % (10001 - len(s1))
            s2 = s2[:cut] + "".join(shuffled) + s2[cut + len(s1):]
        pairs.append((s1, s2))
    found = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            s1, s2 = pairs[(rnd * 7 + g) % count]
            got = check_inclusion(s1, s2)
            if got:
                found += 1
            checksum = (checksum * 31 + (g + 2 if got else 1)) % 1000000007
    print(f"{count} pairs, {rounds} rounds: {found} found, checksum {checksum}")


main()
