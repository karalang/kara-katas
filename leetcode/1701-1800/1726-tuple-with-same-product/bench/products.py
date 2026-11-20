# LeetCode #1726: Tuple with Same Product -- the bench (products.kara):
# every pair's product counted in a hash map, each new pair meeting the
# earlier pairs of its product, 8 tuples each.


def tuple_same_product(nums):
    counts = {}
    tuples = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            p = nums[i] * nums[j]
            seen = counts.get(p, 0)
            tuples += 8 * seen
            counts[p] = seen + 1
    return tuples


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 20
    rounds = 3
    n = 1000
    top = 10000
    seed = [1726]
    problems = []
    for _ in range(count):
        pool = list(range(1, top + 1))
        for i in range(n):
            j = i + next_random(seed) % (top - i)
            pool[i], pool[j] = pool[j], pool[i]
        problems.append(pool[:n])
    total = 0
    check = 0
    for r in range(rounds):
        for nums in problems:
            answer = tuple_same_product(nums)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {n} values up to {top}, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
