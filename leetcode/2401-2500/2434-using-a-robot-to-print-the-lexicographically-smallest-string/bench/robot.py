# LeetCode #2434: Using a Robot to Print the Lexicographically Smallest
# String -- the bench, the ★ arm: the letters left counted, a pointer at
# the smallest with a count, and `t` popped after each push while its
# top is no larger.


def robot_with_string(b):
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
    return paper


seed = 2434


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    word = [97 + next_random() % 8 for _ in range(100000)]
    check = 0
    for p in range(300):
        word[(p * 7919) % 100000] = 97 + p % 8
        paper = robot_with_string(word)
        for c in paper:
            check = (check * 31 + c) % 1000000007
    print(f"300 passes over 10^5 letters: checksum {check}")


main()
