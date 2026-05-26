# Benchmark workload — greedy Integer to Roman (LeetCode #12).
# Python mirror of bench/greedy.kara. Same K (scaled 10× down), same LCG
# fill, same sink formula — see that file's header for the workload
# rationale.
#
# CPython at K=10M would take multi-second per sample; bench.sh runs this
# at K=1M (scale = 10×) and the README quotes the projected K=10M wall
# for the ergonomic-foil comparison.


def int_to_roman(num: int) -> list[int]:
    out: list[int] = []
    n = num
    while n >= 1000: out.append(ord('M')); n -= 1000
    if    n >= 900:  out.append(ord('C')); out.append(ord('M')); n -= 900
    if    n >= 500:  out.append(ord('D')); n -= 500
    if    n >= 400:  out.append(ord('C')); out.append(ord('D')); n -= 400
    while n >= 100:  out.append(ord('C')); n -= 100
    if    n >= 90:   out.append(ord('X')); out.append(ord('C')); n -= 90
    if    n >= 50:   out.append(ord('L')); n -= 50
    if    n >= 40:   out.append(ord('X')); out.append(ord('L')); n -= 40
    while n >= 10:   out.append(ord('X')); n -= 10
    if    n >= 9:    out.append(ord('I')); out.append(ord('X')); n -= 9
    if    n >= 5:    out.append(ord('V')); n -= 5
    if    n >= 4:    out.append(ord('I')); out.append(ord('V')); n -= 4
    while n >= 1:    out.append(ord('I')); n -= 1
    return out


def score_roman(r: list[int]) -> int:
    return sum(r)


def main() -> None:
    k_iters = 1_000_000  # 10× scaled down vs the compiled mirrors
    sum_v = 0
    for k in range(k_iters):
        raw = k * 2654435769 + 305419896
        num = (raw % 3999 + 3999) % 3999 + 1
        r = int_to_roman(num)
        sum_v += score_roman(r)
    print(sum_v)


if __name__ == "__main__":
    main()
