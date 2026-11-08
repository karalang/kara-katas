# LeetCode #2011: Final Value of Variable After Performing Operations -- a
# mirror of the ★ arm, final_value.kara.


def final_value_after_operations(operations):
    x = 0
    for op in operations:
        if op in ("++X", "X++"):
            x += 1
        elif op in ("--X", "X--"):
            x -= 1
    return x


seed = 2011


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def rem(a, b):
    # Kāra's `%` keeps the sign of the dividend, as Rust's does
    r = abs(a) % b
    return r if a >= 0 else -r


def mix(check, answer):
    return rem(check * 31 + answer, 1000000007)


def random_operations(n, up):
    forms = ["++X", "X++", "--X", "X--"]
    operations = []
    for _ in range(n):
        down = 0 if next_random() % 10 < up else 2
        operations.append(forms[down + next_random() % 2])
    return operations


def main():
    examples = [
        ["--X", "X++", "X++"],
        ["++X", "++X", "X++"],
        ["X++", "++X", "--X", "X--"],
        ["X--"],
        ["--X", "--X", "X--"],
        ["++X", "--X", "++X", "--X", "X++"],
    ]
    for operations in examples:
        shown = "[" + ", ".join(operations) + "]"
        print(f"{shown} -> {final_value_after_operations(operations)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 100 + 1
        up = next_random() % 11
        answer = final_value_after_operations(random_operations(n, up))
        total += answer
        check = mix(check, answer)
    print(f"3000 lists of 1 to 100 operations: sum {total}, checksum {check}")


main()
