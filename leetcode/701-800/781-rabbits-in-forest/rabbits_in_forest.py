# LeetCode 781 — Rabbits in Forest, groups counted by answer.
# Mirrors rabbits_in_forest.kara (the ★ arm) and its harness.


def num_rabbits(answers):
    count = {}
    for a in answers:
        count[a] = count.get(a, 0) + 1
    total = 0
    for v, c in count.items():
        size = v + 1
        total += (c + size - 1) // size * size
    return total


seed = 781


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(answers):
    print(f"{answers} -> {num_rabbits(answers)}")


def main():
    show([1, 1, 2])
    show([10, 10, 10])
    show([0])
    show([0, 0, 0])
    show([1, 0, 1, 0, 1])
    show([2, 2, 2, 2, 1, 1, 1])
    show([3, 1, 3, 1, 3, 3, 3])
    many = [next_random() % 1000 for _ in range(1000)]
    print(f"1000 answers below 1000 -> {num_rabbits(many)}")
    print(f"1000 answers of 999 -> {num_rabbits([999] * 1000)}")
    print(f"1000 answers of 0 -> {num_rabbits([0] * 1000)}")
    total_sum = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 50
        top = 1 + next_random() % 10
        answers = [next_random() % top for _ in range(n)]
        total = num_rabbits(answers)
        total_sum += total
        check = (check * 31 + total) % 1000000007
    print(f"300 random forests: {total_sum} rabbits, checksum {check}")


main()
