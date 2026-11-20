# LeetCode #1691: Maximum Height by Stacking Cuboids -- the bench's Python
# mirror: the ★ arm on 3000 random sets of 100 cuboids, all drawn first,
# each answered 5 times.


def max_height(cuboids):
    boxes = sorted(sorted(c) for c in cuboids)
    n = len(boxes)
    best = [0] * n
    tallest = 0
    for i in range(n):
        best[i] = boxes[i][2]
        for j in range(i):
            if boxes[j][0] <= boxes[i][0] and boxes[j][1] <= boxes[i][1] and boxes[j][2] <= boxes[i][2]:
                best[i] = max(best[i], best[j] + boxes[i][2])
        tallest = max(tallest, best[i])
    return tallest


seed = 1691


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, size, rounds = 3000, 100, 5
    sets = [[[next_random() % 100 + 1 for _ in range(3)] for _ in range(size)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for cuboids in sets:
            answer = max_height(cuboids)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} sets of {size} cuboids, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
