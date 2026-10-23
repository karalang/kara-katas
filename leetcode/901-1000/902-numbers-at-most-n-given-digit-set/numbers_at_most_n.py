# LeetCode #902: Numbers At Most N Given Digit Set -- Python mirror of the
# lengths-then-digits solution in numbers_at_most_n.kara, with the same
# test harness.
#
# Every number shorter than n is at most n: d^k of length k. Of those as
# long as n, read n's digits from the left: a digit of the set below n's
# can be followed by anything, d^rest ways; a digit equal to n's keeps the
# number on n's digits, and if n's digit is not in the set nothing more
# matches. n itself counts if every one of its digits is in the set.


def at_most_n_given_digit_set(digits, n):
    s = str(n)
    k = len(s)
    d = len(digits)
    count = 0
    power = 1
    for _ in range(1, k):
        power *= d
        count += power
    for i in range(k):
        rest = k - i - 1
        ways = 1
        for _ in range(rest):
            ways *= d
        smaller = 0
        equal = False
        for digit in digits:
            c = digit[0]
            if c < s[i]:
                smaller += 1
            elif c == s[i]:
                equal = True
        count += smaller * ways
        if not equal:
            return count
    return count + 1


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s, n):
    digits = list(s)
    listed = ", ".join(f'"{d}"' for d in digits)
    print(f"digits = [{listed}], n = {n} -> {at_most_n_given_digit_set(digits, n)}")


# a random set of the digits 1 to 9, each in it with chance `keep` in 9,
# at least one, in increasing order
def random_set(keep):
    out = []
    for c in range(1, 10):
        if next_random() % 9 < keep:
            out.append(str(c))
    if not out:
        out.append(str(1 + next_random() % 9))
    return out


# n from 1 to 10^9: random with 1 to 10 digits, or every digit from the
# set but one, which is random
def random_n(digits, from_set):
    length = 1 + next_random() % 10
    n = 0
    odd = next_random() % length
    for i in range(length):
        if from_set and i != odd:
            d = int(digits[next_random() % len(digits)])
        else:
            d = next_random() % 10
        n = n * 10 + d
    return min(max(n, 1), 1000000000)


def main():
    global seed
    show("1357", 100)
    show("149", 1000000000)
    show("7", 8)
    show("5", 5)
    show("5", 4)
    show("123456789", 1000000000)
    show("19", 919)
    show("2468", 2468)
    show("3", 1)
    # random cases: sets of every size, n random or made of the set's
    # digits but one
    seed = 902
    check = 0
    total = 0
    for c in range(2000):
        digits = random_set(1 + c % 9)
        n = random_n(digits, c % 2 == 0)
        got = at_most_n_given_digit_set(digits, n)
        total += got
        check = (check * 1000003 + got) % 1000000007
    print(f"2000 cases: counts summing to {total}, checksum {check}")


main()
