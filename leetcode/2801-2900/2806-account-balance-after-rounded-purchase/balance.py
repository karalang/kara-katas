# LeetCode #2806: Account Balance After Rounded Purchase -- the Python
# mirror of the ★ arm: 5 added before the integer division by 10, and the
# rounded amount taken from 100.


def account_balance_after_purchase(purchase_amount):
    return 100 - (purchase_amount + 5) // 10 * 10


seed = 2806


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for p in [9, 15, 0, 100, 5, 95]:
        print(account_balance_after_purchase(p))
    total = 0
    check = 0
    for p in range(101):
        b = account_balance_after_purchase(p)
        total += b
        check = (check * 31 + b) % 1000000007
    print(f"0 to 100: balances sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(3000):
        b = account_balance_after_purchase(next_random() % 101)
        total += b
        check = (check * 31 + b) % 1000000007
    print(f"3000 random amounts: balances sum to {total}, checksum {check}")


main()
