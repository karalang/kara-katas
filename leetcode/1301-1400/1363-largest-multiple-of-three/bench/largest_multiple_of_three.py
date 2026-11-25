# LeetCode #1363 bench -- Python: the digits counted, the sum's residue put
# right by dropping the smallest one or two digits that do it.


def largest_multiple_of_three(digits):
    count = [0] * 10
    total = 0
    for d in digits:
        count[d] += 1
        total += d
    r = total % 3
    if r != 0:
        dropped = False
        for d in (r, r + 3, r + 6):
            if count[d] > 0:
                count[d] -= 1
                dropped = True
                break
        left = 0 if dropped else 2
        for d in (3 - r, 6 - r, 9 - r):
            while left > 0 and count[d] > 0:
                count[d] -= 1
                left -= 1
    out = "".join(str(d) * count[d] for d in range(9, -1, -1))
    if out.startswith("0"):
        return "0"
    return out


seed = 1363


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 arrays of 10^4 digits, the constraints' most, built once; then
    # 10^4 rounds, each setting one digit of one array, both drawn from
    # the checksum so far, and folding the answer's length and three of
    # its digits into the checksum
    arrays = [[next_random() % 10 for _ in range(10000)] for _ in range(20)]
    check = 0
    for r in range(10000):
        k = check % 20
        arrays[k][(check // 20) % 10000] = (check // 200000) % 10
        answer = largest_multiple_of_three(arrays[k]).encode()
        n = len(answer)
        picks = 0 if n == 0 else answer[0] * 7 + answer[n // 2] * 11 + answer[n - 1] * 13
        check = (check * 31 + n + picks + r) % 1000000007
    print(f"10000 rounds over 20 arrays of 10^4 digits: checksum {check}")


main()
