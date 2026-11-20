# LeetCode #1726: Tuple with Same Product -- the Python mirror of the ★
# arm, products.kara: every pair's product counted in a dict, each new
# pair meeting the earlier pairs of its product, 8 tuples each.


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


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        pool = list(range(1, top + 1))
        for i in range(n):
            j = i + next_random(seed) % (top - i)
            pool[i], pool[j] = pool[j], pool[i]
        nums = pool[:n]
        answer = tuple_same_product(nums)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} problems of up to {most} values up to {top}: answers sum to {total}, checksum {check}")


def main():
    print(tuple_same_product([2, 3, 4, 6]))
    print(tuple_same_product([1, 2, 4, 5, 10]))
    print(tuple_same_product([7]))
    print(tuple_same_product(list(range(1, 13))))
    seed = [1726]
    batch(3000, 10, 20, seed)
    batch(100, 100, 200, seed)
    batch(3, 300, 10000, seed)


main()
