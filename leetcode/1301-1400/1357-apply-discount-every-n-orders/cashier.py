# LeetCode #1357 -- Python mirror of the ★ arm: the prices in a dict from
# product to price, and a count of the customers so far.


class Cashier:
    def __init__(self, n, discount, products, prices):
        self.n = n
        self.discount = discount
        self.served = 0
        self.price = dict(zip(products, prices))

    def get_bill(self, product, amount):
        self.served += 1
        bill = 0.0
        for p, a in zip(product, amount):
            bill += float(self.price[p] * a)
        if self.served % self.n == 0:
            return bill * float(100 - self.discount) / 100.0
        return bill


seed = [1357]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def cents(bill):
    # Rust's f64::round: halves away from zero
    x = bill * 100.0
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    c = Cashier(3, 50, [1, 2, 3, 4, 5, 6, 7], [100, 200, 300, 400, 300, 200, 100])
    bills = [
        c.get_bill([1, 2], [1, 2]),
        c.get_bill([3, 7], [10, 10]),
        c.get_bill([1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1, 1]),
        c.get_bill([4], [10]),
        c.get_bill([7, 3], [10, 10]),
        c.get_bill([7, 5, 3, 1, 6, 4, 2], [10, 10, 10, 9, 9, 9, 7]),
        c.get_bill([2, 3, 5], [5, 3, 2]),
    ]
    print(show([cents(b) for b in bills]))
    free = Cashier(1, 100, [5], [7])
    full = Cashier(1, 0, [5], [7])
    rare = Cashier(10000, 50, [5], [7])
    ids = list(range(1, 201))
    big = Cashier(1, 99, ids, [1000] * 200)
    most = big.get_bill(ids, [1000] * 200)
    print(f"{cents(free.get_bill([5], [3]))} {cents(full.get_bill([5], [3]))} {cents(rare.get_bill([5], [3]))} {cents(most)}")
    total = 0
    check = 0
    for _ in range(300):
        k = 1 + next_random() % 200
        products = list(range(1, 201))
        for i in range(200):
            j = i + next_random() % (200 - i)
            products[i], products[j] = products[j], products[i]
        products = products[:k]
        prices = [1 + next_random() % 1000 for _ in range(k)]
        n = 1 + next_random() % 10
        discount = next_random() % 101
        cashier = Cashier(n, discount, products, prices)
        for _ in range(1 + next_random() % 40):
            m = 1 + next_random() % 20
            picked = []
            amount = []
            for _ in range(m):
                p = products[next_random() % k]
                if p not in picked:
                    picked.append(p)
                    amount.append(1 + next_random() % 1000)
            got = cents(cashier.get_bill(picked, amount))
            total += got
            check = (check * 131 + got) % 1000000007
    print(f"300 random cashiers: {total} cents billed, checksum {check}")


main()
