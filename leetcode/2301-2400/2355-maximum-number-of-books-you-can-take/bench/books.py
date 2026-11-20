# LeetCode #2355: Maximum Number of Books You Can Take -- the bench, the ★
# arm in Python: the most books from a run ending at each shelf, from the
# nearest shelf to the left that caps the run, found on a monotonic stack.


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
    # array a holds 10^5 shelves: up to 10^5 books every (a + 2)^2-th
    # shelf, up to 100 (a + 1) between
    arrays = []
    for a in range(10):
        books = []
        for i in range(100000):
            r = next_random()
            books.append(r * 3 % 100001 if i % ((a + 2) * (a + 2)) == 0 else r % (100 * (a + 1) + 1))
        arrays.append(books)
    check = 0
    for p in range(50):
        for books in arrays:
            check = (check * 31 + maximum_books(books) % 1000000007 + p) % 1000000007
    print(f"50 passes over 10 arrays of 10^5 shelves: checksum {check}")


main()
