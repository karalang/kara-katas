# benchmark's Python mirror of moves.kara (LeetCode #2193, the ★ arm):
# the twin swapped out to the end.


def min_moves_to_make_palindrome(s):
    b = bytearray(s, "ascii")
    left, right, moves = 0, len(b) - 1, 0
    while left < right:
        k = right
        while k > left and b[k] != b[left]:
            k -= 1
        if k == left:
            b[left], b[left + 1] = b[left + 1], b[left]
            moves += 1
            continue
        while k < right:
            b[k], b[k + 1] = b[k + 1], b[k]
            k += 1
            moves += 1
        left += 1
        right -= 1
    return moves


seed = 2193


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word():
    chars = []
    for _ in range(1000):
        c = chr(97 + next_random() % 26)
        chars += [c, c]
    for i in range(1999, 0, -1):
        j = next_random() % (i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def main():
    words = [random_word() for _ in range(20)]
    check = 0
    for r in range(3000):
        check = (check * 31 + min_moves_to_make_palindrome(words[r % 20])) % 1000000007
    print(f"3000 solves: checksum {check}")


main()
