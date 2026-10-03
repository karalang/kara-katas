# LeetCode #338: Counting Bits — Python mirror of counting_bits.kara.
#
# Same recurrence, the same harness and the same output.


def count_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans


def show(n):
    ans = count_bits(n)
    shown = ", ".join(str(c) for c in ans)
    print(f"{n} -> [{shown}]")


def summary(n):
    ans = count_bits(n)
    total = 0
    most = 0
    h = 0
    for c in ans:
        total += c
        most = max(most, c)
        h = (h * 31 + c) % 1000000007
    print(f"{n} -> {len(ans)} counts, total {total}, largest {most}, hash {h}")


def main():
    show(2)
    show(5)
    show(0)
    show(1)
    show(16)
    show(31)
    show(33)
    summary(1000)
    summary(65535)
    summary(65536)
    summary(100000)
    summary(1048575)


main()
