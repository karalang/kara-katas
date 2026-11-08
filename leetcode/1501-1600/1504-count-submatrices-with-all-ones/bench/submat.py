# LeetCode #1504: Count Submatrices With All Ones -- the benchmark,
# the same algorithm as submat.kara: column heights of ones per row, and for each cell the count of
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


def random_square(size, ones):
    return [[1 if next_random() % 100 < ones else 0 for _ in range(size)] for _ in range(size)]


def main():
    mats = [random_square(150, 50 + i % 50) for i in range(400)]
    total = check = 0
    for mat in mats:
        answer = count_submatrices(mat)
        total += answer
        check = mix(check, answer)
    print(f"400 matrices of 150 x 150: sum {total}, checksum {check}")


main()
