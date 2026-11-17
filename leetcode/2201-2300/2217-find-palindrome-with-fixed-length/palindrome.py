# LeetCode #2217: Find Palindrome With Fixed Length -- the mirror of
# palindrome.kara: the q-th half is 10^(half - 1) + q - 1, mirrored by
# arithmetic, the middle digit of an odd length used once.


def kth_palindrome(queries, int_length):
    half = (int_length + 1) // 2
    low = 10 ** (half - 1)
    answer = []
    for q in queries:
        first = low + q - 1
        if first >= low * 10:
            answer.append(-1)
            continue
        palindrome = first
        rest = first // 10 if int_length % 2 == 1 else first
        while rest > 0:
            palindrome = palindrome * 10 + rest % 10
            rest //= 10
        answer.append(palindrome)
    return answer


seed = 2217


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a draw of 30 bits, since one draw stops at 32767
def wide_random():
    return next_random() * 32768 + next_random()


def show(queries, int_length):
    print(f"{queries} of length {int_length} -> {kth_palindrome(queries, int_length)}")


def main():
    # LeetCode's two examples, then four more: length 1 to its end and
    # past it, length 2, the last of length 15, and 10^9
    show([1, 2, 3, 4, 5, 90], 3)
    show([2, 4, 6], 4)
    show([1, 9, 10], 1)
    show([1, 9, 10], 2)
    show([90000000, 90000001], 15)
    show([1000000000, 1], 15)
    # 3000 random cases of 1 to 20 queries of length 1 to 15, each query
    # up to twice the palindromes of that length, and at most 10^9
    check = 0
    for _ in range(3000):
        int_length = next_random() % 15 + 1
        k = next_random() % 20 + 1
        count = 9 * 10 ** ((int_length - 1) // 2)
        queries = [wide_random() % min(2 * count, 1000000000) + 1 for _ in range(k)]
        for p in kth_palindrome(queries, int_length):
            check = (check * 31 + p + 1) % 1000000007
    print(f"3000 cases: checksum {check}")
    # the constraints' largest: 5 * 10^4 queries of length 15 up to 10^9,
    # and 5 * 10^4 of length 14 counting up from 1
    wide = []
    counting = []
    for i in range(50000):
        wide.append(wide_random() % 1000000000 + 1)
        counting.append(i + 1)
    long = kth_palindrome(wide, 15)
    found = sum(1 for p in long if p != -1)
    total = sum(p % 1000000007 for p in long if p != -1) % 1000000007
    even = kth_palindrome(counting, 14)
    print(f"5 * 10^4 of length 15: {found} found, sum {total}; 5 * 10^4 of length 14: last {even[49999]}")


main()
