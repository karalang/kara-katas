# Benchmark for #451: mirror of frequency_sort.kara (count, then sort
# the distinct characters) on 20 random strings of 200,000 characters,
# built once, then each sorted 5 times.


def frequency_sort(s):
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    order = sorted((-n, c) for c, n in counts.items())
    return "".join(c * -negative for negative, c in order)


seed = 451


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    count = 20
    n = 200000
    rounds = 5
    strings = []
    for i in range(count):
        # From the first 3, 10, 30 or all 62 characters, in turn.
        k = [3, 10, 30, 62][i % 4]
        strings.append("".join(alphabet[next_random() % k] for _ in range(n)))
    characters = 0
    checksum = 0
    for _ in range(rounds):
        for s in strings:
            out = frequency_sort(s)
            characters += len(out)
            sample = ord(out[0]) * 65536 + ord(out[len(out) // 2]) * 256 + ord(out[-1])
            checksum = (checksum * 31 + len(out) + sample) % 1000000007
    print(f"{rounds} rounds on {count} strings of {n}: {characters} characters, checksum {checksum}")


main()
