# LeetCode 791 — Custom Sort String: the bench, in Python.
# Mirrors custom_sort_string.kara: count the letters, write out order's
# letters, then the rest in place, into a new string each round.


def custom_sort_string(order, s):
    count = [0] * 26
    for c in s:
        count[ord(c) - 97] += 1
    named = [False] * 26
    out = []
    for c in order:
        at = ord(c) - 97
        named[at] = True
        for _ in range(count[at]):
            out.append(c)
    for c in s:
        if not named[ord(c) - 97]:
            out.append(c)
    return "".join(out)


seed = 791


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    orders = []
    strings = []
    for _ in range(64):
        pool = list(letters)
        i = 25
        while i > 0:
            j = next_random() % (i + 1)
            pool[i], pool[j] = pool[j], pool[i]
            i -= 1
        size = 1 + next_random() % 26
        orders.append("".join(pool[:size]))
        strings.append("".join(letters[next_random() % 26] for _ in range(200)))
    rounds = 1000000
    total = 0
    check = 0
    for r in range(rounds):
        answer = custom_sort_string(orders[r % 64], strings[(r // 64) % 64])
        total += len(answer)
        if r % 1000 == 0:
            for b in answer.encode():
                check = (check * 131 + b) % 1000000007
    print(f"{rounds} rounds of 200-letter strings: {total} letters, checksum {check}")


main()
