# LeetCode #932: Beautiful Array -- bench: divide and conquer with a
# memo. Mirrors beautiful_array.kara, .c, .rs and go-seq/.


def build(n, memo):
    if n in memo:
        return list(memo[n])
    out = []
    if n == 1:
        out.append(1)
    else:
        for x in build((n + 1) // 2, memo):
            out.append(2 * x - 1)
        for x in build(n // 2, memo):
            out.append(2 * x)
    memo[n] = list(out)
    return out


def beautiful_array(n):
    return build(n, {})


def main():
    rounds = 100
    top = 1000
    total = 0
    check = 0
    for r in range(rounds):
        # each round builds the array for every n from 1 to top, starting
        # from a different n
        for i in range(top):
            n = (r + i) % top + 1
            nums = beautiful_array(n)
            total += nums[n // 2]
            check = (check * 1000003 + nums[n - 1]) % 1000000007
    print(f"{rounds} rounds over n from 1 to {top}: middles summing to {total}, checksum {check}")


main()
