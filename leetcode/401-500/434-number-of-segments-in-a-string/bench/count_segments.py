# Benchmark for #434: mirror of count_segments.kara (counting starts)
# on 10,000 windows of one random text of 1,000,000 characters.


def count_segments(s):
    count = 0
    for i in range(len(s)):
        if s[i] != " " and (i == 0 or s[i - 1] == " "):
            count += 1
    return count


seed = 434


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 1000000
    windows = 10000
    letters = "abcdefghijklmnopqrstuvwxyz"
    # Words of 1 to 8 letters between runs of 1 to 3 spaces.
    parts = []
    length_so_far = 0
    while length_so_far < size:
        word = 1 + next_random() % 8
        for _ in range(word):
            if length_so_far < size:
                parts.append(letters[next_random() % 26])
                length_so_far += 1
        gap = 1 + next_random() % 3
        for _ in range(gap):
            if length_so_far < size:
                parts.append(" ")
                length_so_far += 1
    text = "".join(parts)
    total = 0
    checksum = 0
    for _ in range(windows):
        length = next_random() % 100001
        start = next_random() % (size - length + 1)
        n = count_segments(text[start:start + length])
        total += n
        checksum = (checksum * 31 + n) % 1000000007
    print(f"{windows} windows of a text of {size}: {total} segments, checksum {checksum}")


main()
