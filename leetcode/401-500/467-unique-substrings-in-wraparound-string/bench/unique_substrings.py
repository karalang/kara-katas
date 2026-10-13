# Benchmark for #467: mirror of unique_substrings.kara (the ★ arm: the
# longest run ending at each letter) on the same workload.


def find_substring_in_wrapround_string(s):
    longest = [0] * 26
    run = 0
    previous = -1
    for c in s:
        code = ord(c) - 97
        if previous >= 0 and code == (previous + 1) % 26:
            run += 1
        else:
            run = 1
        longest[code] = max(longest[code], run)
        previous = code
    total = 0
    for length in longest:
        total += length
    return total


seed = 467


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(i):
    return chr(97 + i % 26)


def main():
    count = 10
    n = 100000
    rounds = 100
    strings = []
    for _ in range(count):
        letters = []
        last = next_random() % 26
        letters.append(letter(last))
        for _ in range(1, n):
            if next_random() % 16 == 0:
                last = next_random() % 26
            else:
                last = (last + 1) % 26
            letters.append(letter(last))
        strings.append("".join(letters))
    total = 0
    checksum = 0
    for _ in range(rounds):
        for k in range(count):
            strings[k] = strings[k] + letter(next_random() % 26)
            found = find_substring_in_wrapround_string(strings[k])
            total += found
            checksum = (checksum * 31 + found) % 1000000007
    print(f"{rounds} rounds on {count} strings: {total} substrings in all, checksum {checksum}")


main()
