# Python mirror of moves.kara (LeetCode #2193, the ★ arm): matched from
# the outside in, the leftmost letter's nearest twin from the right end
# swapped out to the end; a letter with no twin swapped one step inward.


def min_moves_to_make_palindrome(s):
    b = list(s)
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


def random_word(n, letters):
    chars = []
    for _ in range(n // 2):
        c = chr(97 + next_random() % letters)
        chars += [c, c]
    if n % 2 == 1:
        chars.append(chr(97 + next_random() % letters))
    for i in range(len(chars) - 1, 0, -1):
        j = next_random() % (i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def show(s):
    print(f"{s} -> {min_moves_to_make_palindrome(s)}")


for w in ["aabb", "letelt", "z", "racecar", "xaa", "abcdcbaabcdcba", "abab", "bbaaddcc"]:
    show(w)
total = check = 0
for rnd in range(3000):
    n = next_random() % 40 + 1
    letters = [2, 5, 26][rnd % 3]
    s = random_word(n, letters)
    m = min_moves_to_make_palindrome(s)
    total += m
    check = (check * 31 + m + n) % 1000000007
print(f"3000 words: {total} moves, checksum {check}")
wide = random_word(2000, 26)
narrow = random_word(2000, 2)
half = random_word(1000, 26)
doubled = half + half
print(f"2000 letters: {min_moves_to_make_palindrome(wide)} {min_moves_to_make_palindrome(narrow)} {min_moves_to_make_palindrome(doubled)}")
