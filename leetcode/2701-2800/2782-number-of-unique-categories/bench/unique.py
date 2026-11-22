# LeetCode #2782: Number of Unique Categories -- the bench in Python: the
# ★ arm over 1000 sets of 100 elements from up to 100 categories, all
# drawn first, then each answered 100 times through the judge's handler,
# whose questions are counted.


class CategoryHandler:
    def __init__(self, categories):
        self.categories = categories
        self.asked = 0

    def have_same_category(self, a, b):
        self.asked += 1
        n = len(self.categories)
        return 0 <= a < n and 0 <= b < n and self.categories[a] == self.categories[b]


def number_of_categories(n, handler):
    representatives = []
    for i in range(n):
        if not any(handler.have_same_category(r, i) for r in representatives):
            representatives.append(i)
    return len(representatives)


seed = 2782


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 1000
    rounds = 100
    handlers = []
    for _ in range(count):
        k = next_random() % 100 + 1
        handlers.append(CategoryHandler([next_random() % k for _ in range(100)]))
    total = 0
    check = 0
    for r in range(rounds):
        for handler in handlers:
            a = number_of_categories(100, handler)
            total += a
            check = (check * 31 + a + r) % 1000000007
    asked = sum(h.asked for h in handlers)
    print(f"{count} sets of 100, {rounds} rounds: categories sum to {total} after {asked} questions, checksum {check}")


main()
