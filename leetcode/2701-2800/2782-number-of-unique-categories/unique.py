# LeetCode #2782: Number of Unique Categories -- the ★ arm in Python
# (unique.kara): one representative per category found so far, each new
# element asked against them and made one when it shares with none.


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
    print(number_of_categories(6, CategoryHandler([1, 1, 2, 2, 3, 3])))
    print(number_of_categories(5, CategoryHandler([1, 2, 3, 4, 5])))
    print(number_of_categories(3, CategoryHandler([1, 1, 1])))
    print(number_of_categories(100, CategoryHandler([7] * 100)))
    print(number_of_categories(100, CategoryHandler(list(range(100)))))
    for count, most, kinds in [(3000, 12, 4), (300, 100, 100)]:
        total = 0
        check = 0
        for _ in range(count):
            n = next_random() % 12 + 1 if most == 12 else most
            k = next_random() % kinds + 1
            categories = [next_random() % k for _ in range(n)]
            a = number_of_categories(n, CategoryHandler(categories))
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"{count} sets of up to {most}: categories sum to {total}, checksum {check}")


main()
