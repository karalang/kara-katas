# Benchmark: LeetCode #985 Sum of Even Numbers After Queries -- the ★ arm, a
# running sum, on LeetCode's largest: 10000 values and 10000 queries.
# Mirrors sum_even_after_queries.kara, .rs, .c and go-seq/.


def sum_even_after_queries(nums, queries):
    a = list(nums)
    even = sum(x for x in a if x % 2 == 0)
    answer = []
    for val, index in queries:
        if a[index] % 2 == 0:
            even -= a[index]
        a[index] += val
        if a[index] % 2 == 0:
            even += a[index]
        answer.append(even)
    return answer


seed = 985


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 300
    cases = []
    for _ in range(20):
        nums = [next_random() % 20001 - 10000 for _ in range(10000)]
        queries = []
        for _ in range(10000):
            val = next_random() % 20001 - 10000
            queries.append((val, next_random() % 10000))
        cases.append((nums, queries))
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            nums, queries = cases[(r + i) % 20]
            answer = sum_even_after_queries(nums, queries)
            last = answer[-1]
            total += last
            check = (check * 31 + (last % 1000000007 + 1000000007) % 1000000007) % 1000000007
    print(f"{rounds} rounds over 20 cases of 10000 values and 10000 queries: sum {total}, checksum {check}")


main()
