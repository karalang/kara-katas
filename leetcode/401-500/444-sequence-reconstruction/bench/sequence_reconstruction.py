# Benchmark for #444: mirror of sequence_reconstruction.kara (positions
# and neighbouring pairs) on 50 random cases of n = 5,000, built once
# and answered 30 times over.


def sequence_reconstruction(nums, sequences):
    n = len(nums)
    position = [0] * (n + 1)
    for i in range(n):
        position[nums[i]] = i
    covered = [False] * n
    for s in sequences:
        for j in range(1, len(s)):
            a = position[s[j - 1]]
            b = position[s[j]]
            if a >= b:
                return False
            if b == a + 1:
                covered[a] = True
    for i in range(n - 1):
        if not covered[i]:
            return False
    return True


seed = 444


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 50
    n = 5000
    rounds = 30
    cases_nums = []
    cases_sequences = []
    values = 0
    for c in range(count):
        nums = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        sequences = []
        windows = 1 + next_random() % (n * 2 + 2)
        for _ in range(windows):
            start = next_random() % n
            length = 1 + next_random() % 12
            s = []
            for k in range(start, min(start + length, n)):
                if len(s) == 0 or next_random() % 10 != 0:
                    s.append(nums[k])
            values += len(s)
            sequences.append(s)
        if c % 2 == 0:
            values += n
            sequences.append(list(nums))
        cases_nums.append(nums)
        cases_sequences.append(sequences)
    true_count = 0
    checksum = 0
    for rnd in range(rounds):
        for c in range(count):
            answer = sequence_reconstruction(cases_nums[c], cases_sequences[c])
            if answer:
                true_count += 1
            checksum = (checksum * 31 + c * 2 + (1 if answer else 0) + rnd) % 1000000007
    print(f"{rounds} rounds on {count} cases of n = {n} ({values} values in sequences): {true_count} true, checksum {checksum}")


main()
