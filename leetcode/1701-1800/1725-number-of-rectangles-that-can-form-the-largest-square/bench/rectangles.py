# LeetCode #1725: Number Of Rectangles That Can Form The Largest Square
# -- the bench (rectangles.kara): one pass, the largest shorter side so
# far and how many rectangles give it.


def count_good_rectangles(rectangles):
    best = 0
    count = 0
    for r in rectangles:
        side = min(r[0], r[1])
        if side > best:
            best = side
            count = 1
        elif side == best:
            count += 1
    return count


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 1000
    rounds = 50
    n = 1000
    seed = [1725]
    problems = []
    for _ in range(count):
        rectangles = []
        for _ in range(n):
            l = next_random(seed) % 20 + 1
            w = next_random(seed) % 20 + 1
            rectangles.append([l, w])
        problems.append(rectangles)
    total = 0
    check = 0
    for r in range(rounds):
        for rectangles in problems:
            answer = count_good_rectangles(rectangles)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {n} rectangles, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
