# LeetCode #2217: Find Palindrome With Fixed Length -- bench mirror of
# palindrome.kara: the q-th half is 10^(half - 1) + q - 1, mirrored by
# arithmetic, the middle digit of an odd length used once.


def kth_palindrome(queries, int_length):
    half = (int_length + 1) // 2
    low = 1
    for _ in range(1, half):
        low *= 10
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


# queries up to twice the count of palindromes of the length, so about
# half of them have none
def query(length):
    count = 9
    for _ in range((length - 1) // 2):
        count *= 10
    return wide_random() % (2 * count) + 1


def main():
    lists = []
    for a in range(30):
        # 5 * 10^4 queries for each length from 1 to 15 in turn
        length = a % 15 + 1
        lists.append([query(length) for _ in range(50000)])
    check = 0
    for a in range(30):
        length = a % 15 + 1
        for r in range(10):
            # punch: one query is drawn again before each answer
            lists[a][r * 4999] = query(length)
            for p in kth_palindrome(lists[a], length):
                check = (check * 31 + p + 1) % 1000000007
    print(f"30 lists of 5 * 10^4 queries, 10 punches: checksum {check}")


main()
