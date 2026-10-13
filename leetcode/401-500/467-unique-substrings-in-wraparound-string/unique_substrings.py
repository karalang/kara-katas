# LeetCode #467: Unique Substrings in Wraparound String -- mirror of
# unique_substrings.kara (the star arm: longest run ending at each letter).


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
    return sum(longest)


# ---- test harness ---------------------------------------------------------


def show(s):
    count = find_substring_in_wrapround_string(s)
    if len(s) <= 40:
        print(f'"{s}" -> {count}')
    else:
        print(f'{len(s)} letters from "{s[:10]}" -> {count}')


seed = 467


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(i):
    return chr(97 + i % 26)


def main():
    show("a")
    show("cac")
    show("zab")
    show("abcdefghijklmnopqrstuvwxyz")
    show("zyx")
    show("abcabc")
    show("xyzabcxyz")
    show("aaaaaaaaaa")
    show("".join(letter(25 + i) for i in range(100)))
    show("".join(letter(i + i // 30) for i in range(1000)))
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        n = 1 + next_random() % 200
        breaks = [2, 4, 16][next_random() % 3]
        last = next_random() % 26
        s = [letter(last)]
        for _ in range(1, n):
            if next_random() % breaks == 0:
                last = next_random() % 26
            else:
                last = (last + 1) % 26
            s.append(letter(last))
        found = find_substring_in_wrapround_string("".join(s))
        total += found
        checksum = (checksum * 31 + found) % 1000000007
    print(f"{count} random strings: {total} substrings in all, checksum {checksum}")


main()
