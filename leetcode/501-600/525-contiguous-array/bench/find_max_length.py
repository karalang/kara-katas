# Benchmark for #525: Python mirror of the ★ arm (first index of each
# balance); see find_max_length.kara.


def find_max_length(nums):
    first = {0: -1}
    balance = 0
    best = 0
    for i in range(len(nums)):
        balance += 1 if nums[i] == 1 else -1
        if balance in first:
            best = max(best, i - first[balance])
        else:
            first[balance] = i
    return best


seed = 525


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(20):
        q = 2 + a % 3
        arrays.append([1 if next_random() % q == 0 else 0 for _ in range(100000)])
    total = 0
    checksum = 0
    for _ in range(20):
        for a in range(len(arrays)):
            answer = find_max_length(arrays[a])
            total += answer
            checksum = (checksum * 31 + answer) % 1000000007
    print(f"20 arrays of 100000, 20 rounds: total {total}, checksum {checksum}")


main()
