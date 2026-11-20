# LeetCode #1698: Number of Distinct Substrings in a String -- mirrors
# distinct.kara, the ★ arm: every suffix put in a trie, one node per
# distinct substring.


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


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, letters, seed):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    total = 0
    check = 0
    for _ in range(count):
        n = seed.next() % most + 1
        used = seed.next() % letters + 1
        s = "".join(alphabet[seed.next() % used] for _ in range(n))
        answer = count_distinct(s)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} strings of up to {most} letters from up to {letters}: answers sum to {total}, checksum {check}")


def main():
    print(count_distinct("aabbaba"))
    print(count_distinct("abcdefg"))
    print(count_distinct("a"))
    print(count_distinct("aaaa"))
    print(count_distinct("abab"))
    seed = Seed(1698)
    batch(3000, 12, 4, seed)
    batch(300, 100, 4, seed)
    batch(10, 500, 26, seed)


main()
