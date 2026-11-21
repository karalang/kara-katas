# LeetCode #2411: Smallest Subarrays With Maximum Bitwise OR -- the mirror
# of the ★ arm: walking from the right, the nearest index holding each of
# the 30 bits, the subarray from i reaching the farthest of them.

seed = 2411


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def smallest_subarrays(nums):
    n = len(nums)
    nearest = [-1] * 30
    answer = [1] * n
    for i in range(n - 1, -1, -1):
        reach = i
        for bit in range(30):
            if nums[i] >> bit & 1:
                nearest[bit] = i
            reach = max(reach, nearest[bit])
        answer[i] = reach - i + 1
    return answer


def values(n, top, zeros):
    out = []
    for _ in range(n):
        v = (next_random() * 32768 + next_random()) % top
        out.append(0 if next_random() % zeros == 0 else v)
    return out


def show(answer):
    return ",".join(str(a) for a in answer)


def digest(answer):
    check = 0
    for a in answer:
        check = (check * 31 + a) % 1000000007
    return f"checksum {check}, total {sum(answer)}"


def main():
    print(show(smallest_subarrays([1, 0, 2, 1, 3])))
    print(show(smallest_subarrays([1, 2])))
    print(show(smallest_subarrays([0])))
    print(show(smallest_subarrays([0, 0, 0])))
    print(show(smallest_subarrays([1, 2, 4, 8, 16, 0, 1])))
    print(digest(smallest_subarrays(values(100000, 1000000001, 50))))
    print(digest(smallest_subarrays(values(100000, 16, 3))))
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 64
        for a in smallest_subarrays(values(n, top, 4)):
            total += a
            check = (check * 31 + a) % 1000000007
    print(f"2000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
