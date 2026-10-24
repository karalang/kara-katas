# LeetCode #946: Validate Stack Sequences -- the stack replayed.
#
# Push the values in order, and after each push pop for as long as the
# top of the stack is the next value to be popped. Popping whenever it
# can is never wrong: a value on top that is due now cannot wait, since
# anything pushed after it would bury it. The sequences fit when every
# value has been popped. O(n) time.


def validate_stack_sequences(pushed, popped):
    stack = []
    j = 0
    for v in pushed:
        stack.append(v)
        while len(stack) > 0 and stack[-1] == popped[j]:
            stack.pop()
            j += 1
    return j == len(popped)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n distinct values from 0 to 1000, in a random order.
def random_values(n):
    all_ = list(range(1001))
    for i in range(n):
        j = i + next_random() % (1001 - i)
        all_[i], all_[j] = all_[j], all_[i]
    return all_[:n]


# The pops of a random run of pushes and pops.
def random_run(pushed):
    stack = []
    out = []
    i = 0
    while len(out) < len(pushed):
        if i < len(pushed) and (len(stack) == 0 or next_random() % 2 == 0):
            stack.append(pushed[i])
            i += 1
        else:
            out.append(stack.pop())
    return out


# A random order of the same values.
def shuffled(values):
    out = list(values)
    for i in range(len(out)):
        j = i + next_random() % (len(out) - i)
        out[i], out[j] = out[j], out[i]
    return out


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def b(x):
    return "true" if x else "false"


def main():
    global seed
    # LeetCode's two examples, then a few more
    examples = [
        [[1, 2, 3, 4, 5], [4, 5, 3, 2, 1]],
        [[1, 2, 3, 4, 5], [4, 3, 5, 1, 2]],
        [[7], [7]],
        [[1, 2], [2, 1]],
        [[1, 2], [1, 2]],
        [[2, 1, 0], [1, 2, 0]],
        [[1, 2, 3], [3, 1, 2]],
        [[0, 1, 2, 3], [1, 0, 3, 2]],
    ]
    for e in examples:
        print(f"{show(e[0])} then {show(e[1])}: {b(validate_stack_sequences(e[0], e[1]))}")
    # 300 random cases of 1 to 12 values, half of them from a real run
    seed = 946
    values = 0
    fits = 0
    check = 0
    for c in range(300):
        n = 1 + next_random() % 12
        pushed = random_values(n)
        popped = random_run(pushed) if c % 2 == 0 else shuffled(pushed)
        ok = validate_stack_sequences(pushed, popped)
        values += n
        if ok:
            fits += 1
        check = (check * 31 + (1 if ok else 2)) % 1000000007
    print(f"300 random cases of {values} values: {fits} fit, checksum {check}")
    # LeetCode's longest, 1000 values
    pushed = random_values(1000)
    run = random_run(pushed)
    print(f"1000 values, a random run: {b(validate_stack_sequences(pushed, run))}")
    swapped = list(run)
    k = 0
    while k + 1 < 1000 and validate_stack_sequences(pushed, swapped):
        swapped = list(run)
        swapped[k], swapped[k + 1] = swapped[k + 1], swapped[k]
        k += 37
    print(f"1000 values, the run with two pops swapped: {b(validate_stack_sequences(pushed, swapped))}")
    reversed_ = [pushed[999 - i] for i in range(1000)]
    print(f"1000 values, popped in reverse: {b(validate_stack_sequences(pushed, reversed_))}")
    print(f"1000 values, popped as pushed: {b(validate_stack_sequences(pushed, pushed))}")
    mixed = shuffled(pushed)
    print(f"1000 values, popped in a random order: {b(validate_stack_sequences(pushed, mixed))}")


main()
