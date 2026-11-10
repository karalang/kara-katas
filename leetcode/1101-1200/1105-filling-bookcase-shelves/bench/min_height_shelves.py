# LeetCode #1105: Filling Bookcase Shelves -- the bench in Python: the ★
# arm (the least height for the first i books over every run ending at
# book i that fits a shelf) over 32 bookcases of 1000 books, each round
# changing one book in every bookcase and solving it again.

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


seed = 1105


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for _ in range(32):
        books = []
        for _ in range(1000):
            t = next_random() % 50 + 1
            books.append([t, next_random() % 1000 + 1])
        cases.append(books)
    total = 0
    check = 0
    for rnd in range(200):
        for j in range(len(cases)):
            at = (rnd * 7919 + j * 104729) % 1000
            cases[j][at][0] = (cases[j][at][0] * 7 + rnd) % 50 + 1
            cases[j][at][1] = (cases[j][at][1] * 13 + j) % 1000 + 1
            h = min_height_shelves(cases[j], 1000)
            total += h
            check = (check * 31 + h) % 1000000007
    print(f"200 rounds over 32 bookcases of 1000 books: heights total {total}, checksum {check}")


main()
