# LeetCode #2806: Account Balance After Rounded Purchase -- the bench in
# Python: the ★ arm over 10^6 amounts from 0 to 100, all drawn first,
# then each answered 100 times into a running checksum.


def account_balance_after_purchase(purchase_amount):
    return 100 - (purchase_amount + 5) // 10 * 10


seed = 2806


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 1000000
    rounds = 100
    amounts = [next_random() % 101 for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for p in amounts:
            b = account_balance_after_purchase(p)
            total += b
            check = (check * 31 + b + r) % 1000000007
    print(f"{count} amounts, {rounds} rounds: balances sum to {total}, checksum {check}")


main()
