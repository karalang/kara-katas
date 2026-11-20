# LeetCode #1698: Number of Distinct Substrings in a String -- the bench's
# Python mirror: the ★ arm on 100 random strings of 500 letters, each from
# the first 2 to 26 letters of the alphabet, all drawn first, each
# answered 3 times.


def count_distinct(s):
    letters = s.encode()
    children = [[0] * 26]
    made = 0
    for start in range(len(letters)):
        node = 0
        for c in letters[start:]:
            edge = c - 97
            if children[node][edge] == 0:
                children.append([0] * 26)
                children[node][edge] = len(children) - 1
                made += 1
            node = children[node][edge]
    return made


seed = 1698


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 100, 3, 500
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    strings = []
    for _ in range(count):
        used = next_random() % 25 + 2
        strings.append("".join(alphabet[next_random() % used] for _ in range(n)))
    total = 0
    check = 0
    for r in range(rounds):
        for s in strings:
            answer = count_distinct(s)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} strings of {n} letters, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
