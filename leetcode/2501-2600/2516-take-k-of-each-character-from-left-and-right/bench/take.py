# LeetCode #2516: Take K of Each Character From Left and Right --
# benchmark mirror of the ★ arm (take.kara): 40 strings of 10^5 letters
# built once, then the passes, each asking every string with a k the
# checksum picks.


def take_characters(s, k):
    n = len(s)
    total = [0, 0, 0]
    for b in s:
        total[b - 97] += 1
    if total[0] < k or total[1] < k or total[2] < k:
        return -1
    inside = [0, 0, 0]
    left = 0
    longest = 0
    for right in range(n):
        c = s[right] - 97
        inside[c] += 1
        while total[c] - inside[c] < k:
            inside[s[left] - 97] -= 1
            left += 1
        longest = max(longest, right - left + 1)
    return n - longest


seed = 2516


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strings = [bytes(97 + next_random() % 3 for _ in range(100000)) for _ in range(40)]
    passes = 7
    check = 0
    for p in range(passes):
        for s in strings:
            check = (check * 31 + take_characters(s, check % 30001) + 1 + p) % 1000000007
    print(f"{passes} passes over 40 strings of 10^5: checksum {check}")


main()
