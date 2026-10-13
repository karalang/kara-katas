# Benchmark for #521: Python mirror of the ★ arm (the whole longer word);
# see find_lus_length.kara.


def find_lus_length(a, b):
    return -1 if a == b else max(len(a), len(b))


seed = 521


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    # 20,000 pairs of 1 to 100 letters from 1 to 3 letters made once (a
    # third equal, a third the first word with a letter added, a third
    # unrelated), then every pair answered in each of 5,000 rounds.
    firsts = []
    seconds = []
    for i in range(20000):
        letters = 1 + next_random() % 3
        a = random_word(1 + next_random() % 100, letters)
        if i % 3 == 0:
            b = a[:]
        elif i % 3 == 1:
            b = a + chr(97 + next_random() % letters)
        else:
            b = random_word(1 + next_random() % 100, letters)
        firsts.append(a)
        seconds.append(b)
    total = 0
    checksum = 0
    for rnd in range(5000):
        for i in range(len(firsts)):
            n = find_lus_length(firsts[i], seconds[i])
            total += n
            checksum = (checksum + (rnd + 1) * (n + 2)) % 1000000007
    print(f"20000 pairs, 5000 rounds: total {total}, checksum {checksum}")


main()
