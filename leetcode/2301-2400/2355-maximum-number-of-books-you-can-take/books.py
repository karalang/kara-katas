# LeetCode #2355: Maximum Number of Books You Can Take -- the Python mirror
# of the ★ arm: the most books taken from a run ending at each shelf, from
# the nearest shelf to the left that would cap the run, found on a
# monotonic stack.


def maximum_books(books):
    n = len(books)
    best = [0] * n
    stack = []
    answer = 0
    for i in range(n):
        while stack and books[stack[-1]] - stack[-1] >= books[i] - i:
            stack.pop()
        if stack:
            j = stack[-1]
            length = i - j
            best[i] = length * books[i] - length * (length - 1) // 2 + best[j]
        else:
            length = min(i + 1, books[i])
            best[i] = length * books[i] - length * (length - 1) // 2
        stack.append(i)
        answer = max(answer, best[i])
    return answer


SEED = [2355]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's three examples; one empty shelf; 2000 shelves rising by
    # one, and falling; 10^5 shelves of up to 10^5 books every 50th and up
    # to 200 between
    print(maximum_books([8, 5, 2, 7, 9]))
    print(maximum_books([7, 0, 3, 4, 5]))
    print(maximum_books([8, 2, 3, 7, 3, 4, 0, 1, 4, 3]))
    print(maximum_books([0]))
    print(maximum_books(list(range(1, 2001))))
    print(maximum_books(list(range(2000, 0, -1))))
    big = []
    for i in range(100000):
        r = next_random()
        big.append(r * 3 % 100001 if i % 50 == 0 else r % 201)
    print(maximum_books(big))
    # 2000 random arrays of 1 to 30 shelves of 0 to 1 up to 0 to 40 books
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        top = 2 + next_random() % 40
        books = [next_random() % top for _ in range(n)]
        m = maximum_books(books)
        check = (check * 31 + m) % 1000000007
        total += m
    print(f"2000 arrays: checksum {check}, books {total}")


main()
