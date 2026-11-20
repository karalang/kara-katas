# LeetCode #2384: Largest Palindromic Number -- the bench, the ★ arm in
# Python: the digits counted, the left half from 9 down with no 0
# leading, the largest digit left over in the middle, the half reversed
# after it.


def largest_palindromic(num):
    count = [0] * 10
    for c in num:
        count[ord(c) - 48] += 1
    half = []
    for d in range(9, -1, -1):
        if d == 0 and not half:
            break
        for _ in range(count[d] // 2):
            half.append(chr(48 + d))
    out = list(half)
    for d in range(9, -1, -1):
        if count[d] % 2 == 1:
            out.append(chr(48 + d))
            break
    if not out:
        return "0"
    out.extend(reversed(half))
    return "".join(out)


seed = 2384


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 100 strings of 10^4 digits, string s's below 1 + s % 10, each a 0
    # with a chance of s % 7 in 10; each pass folds every answer's length
    # and middle digit
    strings = []
    for s in range(100):
        b = []
        for _ in range(10000):
            if next_random() % 10 < s % 7:
                b.append("0")
            else:
                b.append(chr(48 + next_random() % (1 + s % 10)))
        strings.append("".join(b))
    check = 0
    for p in range(200):
        for s in range(100):
            answer = largest_palindromic(strings[s])
            check = (check * 31 + len(answer) + ord(answer[len(answer) // 2]) + p) % 1000000007
    print(f"200 passes over 100 strings of 10^4 digits: checksum {check}")


main()
