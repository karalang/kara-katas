/* Benchmark workload — Maximum Product Subarray, O(n) running max/min DP.
 * Algorithmic mirror of bench/max_product.kara / .rs / .py / go-seq. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static inline int64_t imax(int64_t a, int64_t b) { return a > b ? a : b; }
static inline int64_t imin(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t max_product(const int64_t *nums, int64_t n) {
    if (n == 0) return 0;
    int64_t best = nums[0], cur_max = nums[0], cur_min = nums[0];
    for (int64_t i = 1; i < n; i++) {
        int64_t x = nums[i];
        if (x < 0) { int64_t t = cur_max; cur_max = cur_min; cur_min = t; }
        cur_max = imax(x, cur_max * x);
        cur_min = imin(x, cur_min * x);
        if (cur_max > best) best = cur_max;
    }
    return best;
}

int main(void) {
    const int64_t N = 2000000;
    int64_t *data = malloc((size_t)N * sizeof(int64_t));
    int64_t state = 12345;
    for (int64_t i = 0; i < N; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        data[i] = (state % 5) - 2;
    }
    int64_t sum = 0;
    for (int k = 0; k < 10; k++) sum += max_product(data, N);
    printf("%lld\n", (long long)sum);
    free(data);
    return 0;
}
