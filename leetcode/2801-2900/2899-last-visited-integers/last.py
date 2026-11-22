# LeetCode #2899: Last Visited Integers -- the Python mirror of the ★ arm
# (last.kara): the integers kept in the order they come, the run of -1s
# counted, the k-th read back from the end.


def last_visited_integers(nums):
    seen = []
    ans = []
    k = 0
    for v in nums:
        if v == -1:
            k += 1
            ans.append(seen[len(seen) - k] if k <= len(seen) else -1)
        else:
            seen.append(v)
            k = 0
    return ans


seed = 0
total = 0
check = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digest(ans):
    global total, check
    check = (check * 31 + len(ans)) % 1000000007
    for v in ans:
        total += v
        check = (check * 31 + v + 2) % 1000000007


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed, total, check
    print(f"{show(last_visited_integers([1, 2, -1, -1, -1]))} {show(last_visited_integers([1, -1, 2, -1, -1]))}")
    every = [-1] * 100
    half = [i + 1 if i < 50 else -1 for i in range(100)]
    turns = [i + 1 if i % 2 == 0 else -1 for i in range(100)]
    for nums in [every, half, turns]:
        ans = last_visited_integers(nums)
        print(f"{len(ans)} answers: first {ans[0]}, last {ans[-1]}")
    seed = 2899
    total = 0
    check = 0
    for c in range(4000):
        small = c < 3000
        n = next_random() % 10 + 1 if small else 100
        nums = []
        for _ in range(n):
            if small:
                nums.append(-1 if next_random() % 2 == 0 else next_random() % 5 + 1)
            elif next_random() % 3 == 0:
                nums.append(-1)
            else:
                nums.append(next_random() % 100 + 1)
        digest(last_visited_integers(nums))
        if c == 2999:
            print(f"3000 small arrays: answers total {total}, checksum {check}")
            total = 0
            check = 0
    print(f"1000 arrays of 100: answers total {total}, checksum {check}")


main()
