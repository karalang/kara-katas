# LeetCode #1357 -- bench, Python: the prices in a dict from product to
# price, and a count of the customers so far.


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
    x = bill * 100.0
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def main():
    # 20 cashiers, each selling the products 1 to 200 at prices from 1 to
    # 1000, with n from 1 to 10 and a discount from 0 to 100, built once;
    # then 10^6 bills, each of 1 to 20 products bought 1 to 1000 times,
    # all drawn from the checksum so far, every bill folded into it in cents
    cashiers = []
    lists = []
    for _ in range(20):
        products = list(range(1, 201))
        for i in range(200):
            j = i + next_random() % (200 - i)
            products[i], products[j] = products[j], products[i]
        prices = [1 + next_random() % 1000 for _ in range(200)]
        n = 1 + next_random() % 10
        discount = next_random() % 101
        cashiers.append(Cashier(n, discount, products, prices))
        lists.append(products)
    check = 0
    for r in range(1000000):
        k = check % 20
        m = 1 + (check // 20) % 20
        product = [lists[k][(check // 7 + j * 37) % 200] for j in range(m)]
        amount = [1 + (check + j) % 1000 for j in range(m)]
        check = (check * 31 + cents(cashiers[k].get_bill(product, amount)) + r) % 1000000007
    print(f"1000000 bills over 20 cashiers: checksum {check}")


main()
