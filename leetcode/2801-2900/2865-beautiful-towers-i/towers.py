# LeetCode #2865: Beautiful Towers I -- the Python mirror of the ★ arm
# (towers.kara): a stack of indices with rising heights finds the last
# no-taller tower each way, left[i] = left[j] + (i - j) * h[i].


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


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(
        f"{maximum_sum_of_heights([5, 3, 4, 1, 1])} {maximum_sum_of_heights([6, 5, 3, 9, 2, 7])} {maximum_sum_of_heights([3, 2, 5, 5, 2, 3])}"
    )
    n = 1000
    print(
        f"{maximum_sum_of_heights([1000000000] * n)} {maximum_sum_of_heights(list(range(1, n + 1)))} {maximum_sum_of_heights([abs(i - 500) + 1 for i in range(n)])}"
    )
    seed = 2865
    total = 0
    check = 0
    for c in range(3030):
        small = c < 3000
        n = next_random() % 8 + 1 if small else next_random() % 901 + 100
        top = 6 if small else (1000000000 if c % 2 == 0 else 50)
        heights = [wide() % top + 1 for _ in range(n)]
        best = maximum_sum_of_heights(heights)
        total += best
        check = (check * 31 + best) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: sums total {total}, checksum {check}")
            total = 0
            check = 0
    print(f"30 long arrays: sums total {total}, checksum {check}")


main()
