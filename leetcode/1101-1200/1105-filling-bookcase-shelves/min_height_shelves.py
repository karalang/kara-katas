# LeetCode #1105: Filling Bookcase Shelves -- Python mirror of the ★ arm:
# the least height for the first i books, over every run of books ending
# at book i that fits one shelf. Same cases and output as
# min_height_shelves.kara.

I64_MAX = (1 << 63) - 1


def min_height_shelves(books, shelf_width):
    n = len(books)
    best = [0] * (n + 1)
    for i in range(1, n + 1):
        width = 0
        tallest = 0
        best[i] = I64_MAX
        j = i
        while j > 0 and width + books[j - 1][0] <= shelf_width:
            width += books[j - 1][0]
            tallest = max(tallest, books[j - 1][1])
            best[i] = min(best[i], best[j - 1] + tallest)
            j -= 1
    return best[n]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_books(n, width, top):
    books = []
    for _ in range(n):
        t = next_random() % width + 1
        h = next_random() % top + 1
        books.append([t, h])
    return books


def main():
    global seed
    cases = [
        ([[1, 1], [2, 3], [2, 3], [1, 1], [1, 1], [1, 1], [1, 2]], 4),
        ([[1, 3], [2, 4], [3, 2]], 6),
        ([[1, 1]], 1),
        ([[5, 7]], 5),
        ([[1, 2], [1, 3]], 1),
        ([[1, 2], [1, 3]], 2),
        ([[3, 1], [3, 9], [3, 1]], 6),
        ([[2, 9], [1, 1], [1, 1], [2, 9]], 4),
        ([[1, 1], [1, 1], [1, 1000], [1, 1], [1, 1]], 2),
        ([[1000, 1000], [1000, 1000]], 1000),
    ]
    for books, width in cases:
        print(min_height_shelves(books, width))
    seed = 1105
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 40 + 1
        width = next_random() % 30 + 1
        books = random_books(n, width, 20)
        h = min_height_shelves(books, width)
        total += h
        check = (check * 31 + h) % 1000000007
    print(f"2000 random bookcases: heights total {total}, checksum {check}")
    books = random_books(1000, 1000, 1000)
    print(f"1000 books, shelf 1000: {min_height_shelves(books, 1000)}")
    thin = [[1, i % 997 + 1] for i in range(1000)]
    print(f"1000 thin books, shelf 1000: {min_height_shelves(thin, 1000)}, shelf 7: {min_height_shelves(thin, 7)}")


main()
