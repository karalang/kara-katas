# LeetCode #2164: Sort Even and Odd Indices Independently -- the Python
# mirror of parity.kara, the ★ arm: the even places sorted rising, the
# odd ones falling, woven back by place.


def sort_even_odd(nums):
    even = sorted(nums[0::2])
    odd = sorted(nums[1::2], reverse=True)
    return [even[i // 2] if i % 2 == 0 else odd[i // 2] for i in range(len(nums))]


seed = 2164


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> [{', '.join(map(str, sort_even_odd(nums)))}]")


def fold(out, check):
    for x in out:
        check = (check * 31 + x) % 1000000007
    return check


def main():
    show([4, 1, 2, 3])
    show([2, 1])
    show([7])
    show([3, 9])
    show([1, 9, 2, 8, 3, 7])
    show([5, 5, 5, 5, 5])
    check = 0
    for rnd in range(2000):
        length = next_random() % 12 + 1
        most = [3, 10, 100][rnd % 3]
        nums = [next_random() % most + 1 for _ in range(length)]
        check = fold(sort_even_odd(nums), check)
    print(f"2000 lists: checksum {check}")
    rand = [next_random() % 100 + 1 for _ in range(100)]
    print(f"100 at random: checksum {fold(sort_even_odd(rand), 0)}")
    falling = [100 - i for i in range(100)]
    print(f"100 falling: [{', '.join(map(str, sort_even_odd(falling)))}]")
    rising = [i + 1 for i in range(100)]
    print(f"100 rising: checksum {fold(sort_even_odd(rising), 0)}")


main()
