# Benchmark for #659: the greedy, as the Kara ★ arm.


def is_possible(nums):
    left = {}
    for x in nums:
        left[x] = left.get(x, 0) + 1
    ends = {}
    for x in nums:
        if left.get(x, 0) == 0:
            continue
        left[x] -= 1
        if ends.get(x - 1, 0) > 0:
            ends[x - 1] -= 1
            ends[x] = ends.get(x, 0) + 1
        elif left.get(x + 1, 0) > 0 and left.get(x + 2, 0) > 0:
            left[x + 1] -= 1
            left[x + 2] -= 1
            ends[x + 2] = ends.get(x + 2, 0) + 1
        else:
            return False
    return True


seed = 659


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    inputs, rounds = 8, 40
    arrays = []
    for k in range(inputs):
        nums = []
        for _ in range(25000):
            start = next_random() % 20001
            length = 3 + next_random() % 3
            nums.extend(range(start, start + length))
        if k % 2 == 1:
            nums.append(30000)
        nums.sort()
        arrays.append(nums)
    yes = 0
    checksum = 0
    for r in range(rounds):
        pick = (r * 3) % inputs
        ok = is_possible(arrays[pick])
        if ok:
            yes += 1
        checksum = (checksum * 31 + len(arrays[pick]) * 2 + (1 if ok else 0)) % 1000000007
    print(f"{inputs} arrays, {rounds} rounds: {yes} split, checksum {checksum}")


main()
