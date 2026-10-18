// LeetCode #713: Subarray Product Less Than K -- a sliding window.
// Benchmark mirror of the Kara star arm: extend the window right; while
// its product is k or more, drop numbers from the left; count the
// subarrays ending at each right end.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t num_subarray_product_less_than_k(const int64_t *nums,
                                                int64_t n, int64_t k) {
    if (k <= 1) return 0;
    int64_t product = 1, left = 0, count = 0;
    for (int64_t right = 0; right < n; right++) {
        product *= nums[right];
        while (product >= k) {
            product /= nums[left];
            left++;
        }
        count += right - left + 1;
    }
    return count;
}

int main(void) {
    int64_t seed = 713;
    int64_t tops[10] = {2, 3, 5, 10, 20, 50, 100, 200, 500, 1000};
    enum { N = 30000 };
    int64_t *arrays[10];
    for (int t = 0; t < 10; t++) {
        arrays[t] = malloc(N * sizeof(int64_t));
        for (int i = 0; i < N; i++) arrays[t][i] = 1 + next_random(&seed) % tops[t];
    }
    int64_t sum = 0;
    for (int round = 0; round < 200; round++) {
        for (int t = 0; t < 10; t++) sum += num_subarray_product_less_than_k(arrays[t], N, 1000000);
    }
    for (int t = 0; t < 10; t++) free(arrays[t]);
    printf("200 rounds of 10 arrays of 30000, k = 1000000: sum %lld\n", (long long)sum);
    return 0;
}
