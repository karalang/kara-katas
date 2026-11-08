# LeetCode #1504: Count Submatrices With All Ones -- the Python mirror of
# the ★ arm: column heights of ones per row, and for each cell the count of
# all-ones rectangles with that cell as bottom-right corner, from the
# nearest shorter column to its left (a stack of increasing heights).


def count_submatrices(mat):
    m, n = len(mat), len(mat[0])
    heights = [0] * n
    total = 0
    for i in range(m):
        for j in range(n):
            heights[j] = heights[j] + 1 if mat[i][j] == 1 else 0
        ending = [0] * n
        stack = []
        for j in range(n):
            while stack and heights[stack[-1]] >= heights[j]:
                stack.pop()
            if stack:
                k = stack[-1]
                ending[j] = ending[k] + heights[j] * (j - k)
            else:
                ending[j] = heights[j] * (j + 1)
            stack.append(j)
            total += ending[j]
    return total


seed = 1504


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_matrix(most):
    m = next_random() % most + 1
    n = next_random() % most + 1
    ones = next_random() % 101
    return [[1 if next_random() % 100 < ones else 0 for _ in range(n)] for _ in range(m)]


def batch(count, most):
    total = check = 0
    for _ in range(count):
        answer = count_submatrices(random_matrix(most))
        total += answer
        check = mix(check, answer)
    print(f"{count} matrices of up to {most} x {most}: sum {total}, checksum {check}")


def main():
    examples = [[[1, 0, 1], [1, 1, 0], [1, 1, 0]],
                [[0, 1, 1, 0], [0, 1, 1, 1], [1, 1, 1, 0]],
                [[1]], [[0]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                [[1, 1, 1, 1]], [[1], [1], [1]], [[1, 0], [0, 1]]]
    for mat in examples:
        rows = ", ".join("[" + ", ".join(str(x) for x in r) + "]" for r in mat)
        print(f"[{rows}] -> {count_submatrices(mat)}")
    batch(2000, 6)
    batch(100, 40)
    batch(3, 150)


main()
