# LeetCode #1221: Split a String in Balanced Strings -- the Python mirror of
# the ★ arm: walk the string keeping L's count less R's; every time it
# comes back to zero a balanced piece ends. O(n).

seed = 1221


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffled(half):
    letters = []
    for _ in range(half):
        letters.append('L')
        letters.append('R')
    k = len(letters) - 1
    while k > 0:
        j = next_random() % (k + 1)
        letters[k], letters[j] = letters[j], letters[k]
        k -= 1
    return ''.join(letters)


def balanced_string_split(s):
    balance = 0
    pieces = 0
    for c in s:
        balance += 1 if c == 'L' else -1
        if balance == 0:
            pieces += 1
    return pieces


def main():
    for s in ["RLRRLLRLRL", "RLRRRLLRLL", "LLLLRRRR", "RL", "LLRRLR"]:
        print(f"{s}: {balanced_string_split(s)}")
    total = 0
    check = 0
    for _ in range(1000):
        half = next_random() % 8 + 1
        s = shuffled(half)
        answer = balanced_string_split(s)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"1000 random strings up to 16 letters: pieces total {total}, checksum {check}")
    alternating = "LR" * 500
    nested = "L" * 500 + "R" * 500
    wide = shuffled(500)
    print(f"1000 letters, LR over and over: {balanced_string_split(alternating)}, 500 L then 500 R: {balanced_string_split(nested)}, shuffled: {balanced_string_split(wide)}")


main()
