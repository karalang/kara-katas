# LeetCode #2865: Beautiful Towers I -- the bench, as towers.kara: 2000
# arrays of 10^3 towers, each answered 20 times by the stack arm.


def maximum_sum_of_heights(max_heights):
    n = len(max_heights)
    left = [0] * n
    stack = []
    for i in range(n):
        while stack and max_heights[stack[-1]] > max_heights[i]:
            stack.pop()
        if stack:
            j = stack[-1]
            left[i] = left[j] + (i - j) * max_heights[i]
        else:
            left[i] = (i + 1) * max_heights[i]
        stack.append(i)
    stack = []
    best = 0
    right = [0] * n
    for i in range(n - 1, -1, -1):
        while stack and max_heights[stack[-1]] > max_heights[i]:
            stack.pop()
        if stack:
            j = stack[-1]
            right[i] = right[j] + (j - i) * max_heights[i]
        else:
            right[i] = (n - i) * max_heights[i]
        stack.append(i)
        best = max(best, left[i] + right[i] - max_heights[i])
    return best


seed = 2865


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 2000, 20, 1000
    arrays = []
    for c in range(count):
        top = 1000000000 if c % 2 == 0 else 50
        arrays.append([wide() % top + 1 for _ in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        for heights in arrays:
            best = maximum_sum_of_heights(heights)
            total += best
            check = (check * 31 + best % 1000000007 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: sums total {total}, checksum {check}")


main()
