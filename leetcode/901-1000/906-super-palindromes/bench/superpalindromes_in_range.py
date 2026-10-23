# LeetCode #906: Super Palindromes -- bench program, Python.
#
# The palindromic roots built from their first halves, over random ranges
# below 10^18 given as strings. Each query counts the super-palindromes in
# its range and folds the count into a checksum.


def superpalindromes_in_range(left, right):
    lo = int(left)
    hi = int(right)
    count = 0
    for odd in (True, False):
        half = 1
        while True:
            digits = str(half)
            back = digits[::-1]
            tail = back[1:] if odd else back
            root = int(digits + tail)
            if root > hi // root:
                break
            square = root * root
            shown = str(square)
            if square >= lo and shown == shown[::-1]:
                count += 1
            half += 1
    return count


seed = 906


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    queries = 40
    top = 1000000000000000000
    total = 0
    check = 0
    for _ in range(queries):
        a = (next_random() * 32768 + next_random()) * 1073741824 + next_random() * 32768 + next_random()
        b = (next_random() * 32768 + next_random()) * 1073741824 + next_random() * 32768 + next_random()
        a = 1 + a % (top - 1)
        b = 1 + b % (top - 1)
        got = superpalindromes_in_range(str(min(a, b)), str(max(a, b)))
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"{queries} ranges below 10^18: counts summing to {total}, checksum {check}")


main()
