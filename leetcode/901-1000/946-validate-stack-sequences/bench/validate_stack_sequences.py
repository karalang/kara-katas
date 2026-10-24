# Benchmark: LeetCode #946 Validate Stack Sequences -- the ★ arm, the
# stack replayed, on sequences of 1000 values, LeetCode's longest.
# Mirrors validate_stack_sequences.kara, .c, .rs and go-seq/.


def validate_stack_sequences(pushed, popped):
    stack = []
    j = 0
    for v in pushed:
        stack.append(v)
        while len(stack) > 0 and stack[-1] == popped[j]:
            stack.pop()
            j += 1
    return j == len(popped)


seed = 946


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 2500
    count = 20
    n = 1000
    # the values 0 to 1000 in a random order, the first 1000 pushed, and
    # the pops of a random run of pushes and pops, every second one with
    # two neighbouring pops swapped
    pushes = []
    pops = []
    for c in range(count):
        all_ = list(range(1001))
        for i in range(n):
            j = i + next_random() % (1001 - i)
            all_[i], all_[j] = all_[j], all_[i]
        pushed = all_[:n]
        stack = []
        popped = []
        i = 0
        while len(popped) < n:
            if i < n and (len(stack) == 0 or next_random() % 2 == 0):
                stack.append(pushed[i])
                i += 1
            else:
                popped.append(stack.pop())
        if c % 2 == 1:
            k = next_random() % (n - 1)
            popped[k], popped[k + 1] = popped[k + 1], popped[k]
        pushes.append(pushed)
        pops.append(popped)
    fits = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            k = (r + i) % count
            ok = validate_stack_sequences(pushes[k], pops[k])
            if ok:
                fits += 1
            check = (check * 31 + (1 if ok else 2)) % 1000000007
    print(f"{rounds} rounds over {count} pairs of sequences of {n} values: {fits} fit, checksum {check}")


main()
