# LeetCode #2011: Final Value of Variable After Performing Operations -- the
# ★ arm's benchmark, a mirror of final_value.kara.


def final_value_after_operations(operations):
    x = 0
    for op in operations:
        if op == "++X" or op == "X++":
            x += 1
        elif op == "--X" or op == "X--":
            x -= 1
    return x


seed = 2011


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    forms = ["++X", "X++", "--X", "X--"]
    lists = []
    for _ in range(20000):
        up = next_random() % 11
        operations = []
        for _ in range(100):
            down = 0 if next_random() % 10 < up else 2
            operations.append(forms[down + next_random() % 2])
        lists.append(operations)
    calls = 0
    total = 0
    check = 0
    for _ in range(10):
        for a in range(len(lists)):
            answer = final_value_after_operations(lists[a])
            calls += 1
            total += answer
            check = (check * 31 + answer + 100) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
