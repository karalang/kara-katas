# Benchmark workload — two-pointer Container With Most Water (LeetCode #11).
# Python mirror of bench/container.kara. Same N, W, same input fill, same
# sink formula — see that file's header for the workload rationale.
#
# CPython at K=10M takes multi-second per sample; bench.sh runs this
# at K=1M (scale = 10×) and reports the projected K=10M wall in the
# README for the ergonomic-foil comparison.


def max_area_off(heights: list[int], lo: int, hi: int) -> int:
    l = lo
    r = hi
    best = 0
    while l < r:
        h_l = heights[l]
        h_r = heights[r]
        h = h_l if h_l < h_r else h_r
        area = h * (r - l)
        if area > best:
            best = area
        if h_l < h_r:
            l += 1
        else:
            r -= 1
    return best


def main() -> None:
    n = 8
    w = 16
    total = n * w
    k_iters = 1_000_000  # 10× scaled down vs the compiled mirrors

    heights = [0] * total
    for i in range(total):
        raw = i * 2654435769 + 305419896
        v = ((raw % 50) + 50) % 50
        heights[i] = v

    sum_v = 0
    for k in range(k_iters):
        idx = k % n
        lo = idx * w
        hi = lo + w - 1
        sum_v += max_area_off(heights, lo, hi)
    print(sum_v)


if __name__ == "__main__":
    main()
