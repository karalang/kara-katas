# LeetCode #1464 Maximum Product of Two Elements in an Array: a mirror of
# max_product.kara.


def max_product(nums):
    # the product grows with each factor, so it is the two largest values'
    # own: `first` the largest so far and `second` the next, a value above
    # `first` pushing it down
    first = 0
    second = 0
    for x in nums:
        if x > first:
            second = first
            first = x
        elif x > second:
            second = x
    return (first - 1) * (second - 1)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, top):
    return [1 + next_random() % top for _ in range(n)]


def main():
    global seed
    f = max_product
    e = [f([3, 4, 5, 2]), f([1, 5, 4, 5]), f([3, 7]), f([1, 1]), f([1000, 1000]),
         f([1, 1, 1000, 1, 1]), f([1000] * 500)]
    print(" ".join(str(x) for x in e))
    seed = 1464
    most = draw(500, 1000)
    print(f"500 values: {f(most)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = 2 + next_random() % 59
        top = 2 + next_random() % 999
        got = f(draw(n, top))
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"3000 random arrays: total {total}, checksum {check}")


main()
