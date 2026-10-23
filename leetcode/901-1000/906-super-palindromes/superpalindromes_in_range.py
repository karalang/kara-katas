# LeetCode #906: Super Palindromes -- Python mirror of the palindromic roots
# built from their first halves in superpalindromes_in_range.kara, with the
# same test harness.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(left, right):
    print(f'left = "{left}", right = "{right}" -> {superpalindromes_in_range(left, right)}')


def main():
    global seed
    show("4", "1000")
    show("1", "2")
    show("1", "1")
    show("9", "9")
    show("10", "120")
    show("121", "121")
    show("122", "483")
    show("1", "10000")
    show("40804", "44944")
    show("1000000", "999999999")
    seed = 906
    total = 0
    check = 0
    for c in range(60):
        top = 10 ** (1 + c % 12)
        a = 1 + (next_random() * 32768 + next_random()) % top
        b = 1 + (next_random() * 32768 + next_random()) % top
        got = superpalindromes_in_range(str(min(a, b)), str(max(a, b)))
        total += got
        check = (check * 1000003 + got) % 1000000007
    print(f"60 ranges: counts summing to {total}, checksum {check}")
    show("1", "999999999999999999")
    show("10000000000000000", "99999999999999999")
    show("100000000000000000", "999999999999999999")


main()
