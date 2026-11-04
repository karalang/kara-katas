# LeetCode #1047: Remove All Adjacent Duplicates In String -- Python mirror
# of bench/remove_dups.kara: a list as the stack, joined into a string.

seed = 1047


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def remove_duplicates(s):
    stack = []
    for c in s:
        if stack and stack[-1] == c:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


def main():
    count, n, rounds = 100, 200000, 10
    strings = ["".join(chr(ord("a") + next_random() % 4) for _ in range(n)) for _ in range(count)]
    total = check = 0
    for _ in range(rounds):
        for s in strings:
            answer = remove_duplicates(s)
            last = ord(answer[-1]) if answer else 0
            total += len(answer)
            check = (check * 131 + len(answer) + last) % 1000000007
    print(f"{count} strings of {n} letters, {rounds} rounds: total length {total}, checksum {check}")


main()
