# LeetCode #985: Sum of Even Numbers After Queries -- Python mirror of the ★
# arm: the sum of the even values kept as the queries change them, a
# query taking its value out of the sum if it was even and putting it
# back if it is even now. Same cases and output as
# sum_even_after_queries.kara.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def listed(xs):
    return "[" + ", ".join(xs) + "]"


def show(nums, queries):
    got = sum_even_after_queries(nums, queries)
    n = len(got)
    if n > 10:
        shown = f"first {got[0]}, {got[1]}, {got[2]}, last {got[n - 1]} ({n} answers)"
    else:
        shown = listed([str(x) for x in got])
    ns = listed([str(x) for x in nums]) if len(nums) <= 8 else f"{len(nums)} values"
    qs = listed([f"({v}, {i})" for v, i in queries]) if len(queries) <= 8 else f"{len(queries)} queries"
    print(f"nums {ns}, queries {qs} -> {shown}")


def random_case(n, q, top):
    nums = [next_random() % (2 * top + 1) - top for _ in range(n)]
    queries = []
    for _ in range(q):
        val = next_random() % (2 * top + 1) - top
        queries.append((val, next_random() % n))
    return nums, queries


def main():
    global seed
    show([1, 2, 3, 4], [(1, 0), (-3, 1), (-4, 0), (2, 3)])
    show([1], [(4, 0)])
    show([2], [(0, 0)])
    show([1, 3, 5], [(1, 0), (1, 1), (1, 2)])
    show([-2, -3, 4], [(1, 1), (-5, 0), (3, 2)])
    show([7, 7], [(1, 0), (1, 0), (1, 0), (1, 0)])
    show([10000, -10000], [(-10000, 0), (10000, 1), (1, 0), (-1, 1)])
    show([0, 0, 0], [(2, 0), (-2, 0), (3, 2)])
    show([i % 7 - 3 for i in range(10000)], [((i * 37) % 201 - 100, (i * 7919) % 10000) for i in range(10000)])
    show([10000] * 10000, [(-10000 if i % 2 == 0 else 10000, i % 10000) for i in range(10000)])
    seed = 985
    for count, n, q, top in [(300, 8, 8, 10), (3000, 40, 40, 1000), (3, 10000, 10000, 10000)]:
        total = check = answers = 0
        for _ in range(count):
            nn = n if count == 3 else 1 + next_random() % n
            qq = q if count == 3 else 1 + next_random() % q
            nums, queries = random_case(nn, qq, top)
            for x in sum_even_after_queries(nums, queries):
                total += x
                check = (check * 31 + x % 1000000007) % 1000000007
                answers += 1
        print(f"{count} random cases of up to {n} values and {q} queries: {answers} answers, sum {total}, checksum {check}")


main()
