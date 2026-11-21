# LeetCode #2449: Minimum Number of Operations to Make Arrays Similar --
# Python mirror of the ★ arm (similar.kara): the odd and the even values
# of each array sorted and matched in order, the distance over 4.


def make_similar(nums, target):
    odd = sorted(x for x in nums if x % 2 == 1)
    even = sorted(x for x in nums if x % 2 == 0)
    odd_target = sorted(x for x in target if x % 2 == 1)
    even_target = sorted(x for x in target if x % 2 == 0)
    distance = 0
    for i in range(len(odd)):
        distance += abs(odd[i] - odd_target[i])
    for i in range(len(even)):
        distance += abs(even[i] - even_target[i])
    return distance // 4


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    r = next_random()
    return r * 32768 + next_random()


def similar_to(nums, moves, top):
    n = len(nums)
    target = list(nums)
    for _ in range(moves):
        i = wide_random() % n
        j = wide_random() % n
        step = 2 * (1 + next_random() % 50)
        if i != j and target[i] + step <= top and target[j] - step >= 1:
            target[i] += step
            target[j] -= step
    for i in range(n):
        j = i + wide_random() % (n - i)
        target[i], target[j] = target[j], target[i]
    return target


def main():
    global seed
    print(f"example 1: {make_similar([8, 12, 6], [2, 14, 10])}")
    print(f"example 2: {make_similar([1, 2, 5], [4, 1, 3])}")
    print(f"example 3: {make_similar([1, 1, 1, 1, 1], [1, 1, 1, 1, 1])}")
    print(f"one value: {make_similar([7], [7])}")
    print(f"swapped: {make_similar([3, 1000000], [1000000, 3])}")
    print(f"far apart: {make_similar([1, 999999, 2, 1000000], [500001, 499999, 500002, 500000])}")
    print(f"one move each way: {make_similar([1, 999999, 2, 1000000], [3, 999997, 4, 999998])}")
    n = 100000
    seed = 2449
    wide = [1 + wide_random() % 1000000 for _ in range(n)]
    wide_target = similar_to(wide, 200000, 1000000)
    print(f"wide: {make_similar(wide, wide_target)}")
    narrow = [1 + next_random() % 10 for _ in range(n)]
    narrow_target = similar_to(narrow, 100000, 1000000)
    print(f"narrow: {make_similar(narrow, narrow_target)}")
    check = 0
    total = 0
    for _ in range(3000):
        length = 1 + next_random() % 10
        nums = [1 + next_random() % 20 for _ in range(length)]
        moves = next_random() % 10
        target = similar_to(nums, moves, 40)
        answer = make_similar(nums, target)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
