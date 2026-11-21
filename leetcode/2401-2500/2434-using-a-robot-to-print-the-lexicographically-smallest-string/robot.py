# LeetCode #2434: Using a Robot to Print the Lexicographically Smallest
# String -- the Python mirror of the ★ arm: the letters left in `s`
# counted, a pointer kept at the smallest with a count, and `t` popped
# after each push while its top is no larger.

seed = 2434


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def robot_with_string(s):
    b = s.encode()
    left = [0] * 26
    for c in b:
        left[c - 97] += 1
    smallest = 0
    t = []
    paper = []
    for c in b:
        t.append(c)
        left[c - 97] -= 1
        while smallest < 26 and left[smallest] == 0:
            smallest += 1
        while len(t) > 0 and t[-1] - 97 <= smallest:
            paper.append(t.pop())
    return bytes(paper).decode()


def random_word(n, kinds):
    return "".join(chr(97 + next_random() % kinds) for _ in range(n))


def fold(word):
    check = 0
    for b in word.encode():
        check = (check * 31 + b) % 1000000007
    return check


def main():
    for s in ["zza", "bac", "bdda", "q", "abcde", "zyxwvutsrqponmlkjihgfedcba", "bbbba"]:
        print(f"{s}: {robot_with_string(s)}")
    print(f"10^4 random: checksum {fold(robot_with_string(random_word(10000, 26)))}")
    falling = "".join(chr(122 - i % 26) for i in range(10000))
    print(f"10^4 falling: checksum {fold(robot_with_string(falling))}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 12
        kinds = 1 + next_random() % 4
        check = (check * 31 + fold(robot_with_string(random_word(n, kinds)))) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
