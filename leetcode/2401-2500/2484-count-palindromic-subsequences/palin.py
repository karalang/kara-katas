# LeetCode #2484: Count Palindromic Subsequences -- Python mirror of
# palin.kara: by pairs either side of the middle.

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


def random_digits(n, kinds):
    return "".join(str(next_random() % kinds) for _ in range(n))


def main():
    for s in ["103301", "0000000", "9999900000", "1234", "12321", "12345", "01234567899876543210"]:
        print(f"{s} -> {count_palindromes(s)}")
    print(f"\"0\" x 10^4 -> {count_palindromes('0' * 10000)}")
    print(f"\"01\" x 5000 -> {count_palindromes('01' * 5000)}")
    for kinds in [10, 2]:
        s = random_digits(10000, kinds)
        print(f"10^4 random of {kinds} digits -> {count_palindromes(s)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        kinds = 1 + next_random() % 10
        check = (check * 31 + count_palindromes(random_digits(n, kinds))) % MOD
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
