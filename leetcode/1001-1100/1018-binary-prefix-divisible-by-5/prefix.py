# LeetCode #1018: Binary Prefix Divisible By 5 -- running remainder
# Mirrors prefix.kara; its output is byte-identical.


def prefixes_div_by5(nums):
    answer = []
    r = 0
    for bit in nums:
        r = (r * 2 + bit) % 5
        answer.append(r == 0)
    return answer


seed = 1018


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shown(answer):
    return "[" + ", ".join("true" if a else "false" for a in answer) + "]"


def main():
    examples = [
        [0, 1, 1],
        [1, 1, 1],
        [0],
        [1],
        [1, 0, 1],
        [1, 0, 1, 0],
        [1, 1, 1, 1],
        [1, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    ]
    for nums in examples:
        print(f"[{', '.join(str(x) for x in nums)}] -> {shown(prefixes_div_by5(nums))}")
    groups = [(2000, 10, 4), (300, 100, 4), (30, 1000, 4), (30, 1000, 1), (30, 1000, 7), (3, 3000, 4)]
    for count, length, ones in groups:
        trues = longest = check = 0
        for _ in range(count):
            nums = [1 if next_random() % 8 < ones else 0 for _ in range(length)]
            run = 0
            for a in prefixes_div_by5(nums):
                if a:
                    trues += 1
                    run += 1
                    longest = max(longest, run)
                else:
                    run = 0
                check = (check * 2 + (1 if a else 0)) % 1000000007
        print(f"{count} random arrays of {length} bits ({ones}/8 ones): {trues} true, longest run {longest}, checksum {check}")


main()
