// Benchmark workload — two-pointer Container With Most Water (LeetCode #11).
// C mirror of bench/container.kara. Same N, W, K, same input fill, same
// sink formula — see that file's header for the workload rationale.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t max_area_off(const int64_t *heights, int64_t lo, int64_t hi) {
    int64_t l = lo;
    int64_t r = hi;
    int64_t best = 0;
    while (l < r) {
        int64_t h_l = heights[l];
        int64_t h_r = heights[r];
        int64_t h = h_l < h_r ? h_l : h_r;
        int64_t area = h * (r - l);
        if (area > best) {
            best = area;
        }
        if (h_l < h_r) {
            l += 1;
        } else {
            r -= 1;
        }
    }
    return best;
}

int main(void) {
    const int64_t n = 8;
    const int64_t w = 16;
    const int64_t total = n * w;
    const int64_t k_iters = 10000000;

    int64_t *heights = (int64_t *)calloc((size_t)total, sizeof(int64_t));
    for (int64_t i = 0; i < total; i++) {
        int64_t raw = i * 2654435769LL + 305419896LL;
        int64_t v = ((raw % 50) + 50) % 50;
        heights[i] = v;
    }

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % n;
        int64_t lo = idx * w;
        int64_t hi = lo + w - 1;
        sum += max_area_off(heights, lo, hi);
    }
    printf("%lld\n", (long long)sum);
    free(heights);
    return 0;
}
