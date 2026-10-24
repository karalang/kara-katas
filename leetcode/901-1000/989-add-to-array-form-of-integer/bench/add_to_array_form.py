# LeetCode #989: Add to Array-Form of Integer -- bench, the ★ arm
# (k carried in from the last digit), the same algorithm and workload
# as add_to_array_form.kara.


def add_to_array_form(num, k):
    out = []
    carry = k
    i = len(num) - 1
    while i >= 0 or carry > 0:
        if i >= 0:
            carry += num[i]
            i -= 1
        out.append(carry % 10)
        carry //= 10
    out.reverse()
    return out


seed = 989


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_num(n):
    out = []
    for i in range(n):
        d = next_random() % 10
        if i == 0 and d == 0:
            d = 1
        out.append(d)
    return out


def main():
    rounds = 1000
    nums = [random_num(10000) for _ in range(20)]
    digits = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            k = 1 + next_random() % 10000
            got = add_to_array_form(nums[(r + i) % 20], k)
            digits += len(got)
            for j in range(len(got) - 6, len(got)):
                check = (check * 31 + got[j] + 1) % 1000000007
    print(f"{rounds} rounds over 20 numbers of 10000 digits: {digits} digits out, checksum {check}")


main()
