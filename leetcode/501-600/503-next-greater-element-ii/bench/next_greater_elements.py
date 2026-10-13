# Benchmark for #503 in Python: the ★ arm (a stack of indices, twice
# around); see ../next_greater_elements.kara.


def next_greater_elements(nums):
    n = len(nums)
    answer = [-1] * n
    waiting = []
    for i in range(2 * n):
        x = nums[i % n]
        while waiting:
            top = waiting[-1]
            if nums[top] >= x:
                break
            answer[top] = x
            waiting.pop()
        if i < n:
            waiting.append(i)
    return answer


seed = 503


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def rem(a, b):
    # Kāra's % truncates toward zero, as C's does; Python's floors.
    r = abs(a) % b
    return -r if a < 0 else r


def main():
    # 120 arrays of 10,000 numbers (the problem's most), from 0 to 9,
    # from the whole range -10^9 to 10^9, or falling, in turn; built
    # once. Then each array is solved 100 times, the sum of its answers
    # folded into a checksum.
    arrays = 120
    rounds = 100
    n = 10000
    all_nums = []
    for c in range(arrays):
        nums = []
        for i in range(n):
            if c % 3 == 0:
                nums.append(next_random() % 10)
            elif c % 3 == 1:
                hi = next_random()
                nums.append((hi * 65536 + next_random()) % 2000000001 - 1000000000)
            else:
                nums.append(1000000000 - i * 200000 - next_random() % 100000)
        all_nums.append(nums)
    found = 0
    checksum = 0
    for c in range(arrays):
        for _ in range(rounds):
            answer = next_greater_elements(all_nums[c])
            total = 0
            for a in answer:
                total += a
                if a != -1:
                    found += 1
            checksum = (checksum * 31 + rem(total, 1000000007) + 1000000007) % 1000000007
    print(f"{arrays} arrays of {n} numbers, {rounds} times each: {found} with a greater one, checksum {checksum}")


main()
