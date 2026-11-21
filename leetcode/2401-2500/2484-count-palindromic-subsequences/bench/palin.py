# LeetCode #2484: Count Palindromic Subsequences -- bench, Python mirror
# of palin.kara.

MOD = 1000000007


def count_palindromes(s):
    digits = [ord(c) - ord('0') for c in s]
    before_one = [0] * 10
    before_two = [0] * 100
    after_one = [0] * 10
    after_two = [0] * 100
    for d in reversed(digits):
        for a in range(10):
            after_two[d * 10 + a] += after_one[a]
        after_one[d] += 1
    total = 0
    for d in digits:
        after_one[d] -= 1
        for a in range(10):
            after_two[d * 10 + a] -= after_one[a]
        here = 0
        for a in range(10):
            for b in range(10):
                here += before_two[a * 10 + b] * after_two[b * 10 + a]
        total = (total + here) % MOD
        for a in range(10):
            before_two[a * 10 + d] += before_one[a]
        before_one[d] += 1
    return total


seed = 2484


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strings = [[next_random() % 10 for _ in range(2000)] for _ in range(4)]
    check = 0
    for p in range(110):
        for g in range(4):
            strings[g][check % 2000] = check // 2000 % 10
            s = "".join(str(d) for d in strings[g])
            check = (check * 31 + count_palindromes(s) + p) % MOD
    print(f"110 passes over 4 strings of 2000 digits: checksum {check}")


main()
