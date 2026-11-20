# LeetCode #1691: Maximum Height by Stacking Cuboids -- mirrors
# cuboids.kara, the ★ arm: sides sorted, cuboids sorted, the tallest stack
# ending at each.


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


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = seed.next() % most + 1
        cuboids = [[seed.next() % top + 1 for _ in range(3)] for _ in range(n)]
        answer = max_height(cuboids)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} sets of up to {most} cuboids up to {top}: answers sum to {total}, checksum {check}")


def main():
    print(max_height([[50, 45, 20], [95, 37, 53], [45, 23, 12]]))
    print(max_height([[38, 25, 45], [76, 35, 3]]))
    print(max_height([[7, 11, 17], [7, 17, 11], [11, 7, 17], [11, 17, 7], [17, 7, 11], [17, 11, 7]]))
    print(max_height([[1, 2, 3]]))
    seed = Seed(1691)
    batch(3000, 6, 5, seed)
    batch(300, 30, 50, seed)
    batch(30, 100, 100, seed)


main()
