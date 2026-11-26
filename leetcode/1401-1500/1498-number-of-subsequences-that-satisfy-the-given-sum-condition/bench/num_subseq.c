// LeetCode #1498: Number of Subsequences That Satisfy the Given Sum
// Condition -- the bench in C, mirroring num_subseq.kara: the values sorted,
// then two pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000
#define MOD 1000000007LL

static int cmp(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static int32_t num_subseq(const int32_t *nums, int64_t n, int32_t target) {
    int32_t *sorted = malloc(n * sizeof(int32_t));
    memcpy(sorted, nums, n * sizeof(int32_t));
    qsort(sorted, n, sizeof(int32_t), cmp);
    int64_t *pow2 = malloc(n * sizeof(int64_t));
    pow2[0] = 1;
    for (int64_t i = 1; i < n; i++) pow2[i] = pow2[i - 1] * 2 % MOD;
    int64_t count = 0, lo = 0, hi = n - 1;
    while (lo <= hi) {
        if (sorted[lo] + sorted[hi] <= target) {
            count = (count + pow2[hi - lo]) % MOD;
            lo++;
        } else {
            hi--;
        }
    }
    free(sorted);
    free(pow2);
    return (int32_t)count;
}

static int32_t nums[N];

int main(void) {
    int64_t seed = 1498;
    for (int i = 0; i < N; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        nums[i] = (int32_t)(1 + seed / 65536 * 31 % 1000000);
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 200; call++) {
        int64_t at = (check + call * 7919) % N;
        nums[at] = (int32_t)(1 + (check + call) % 1000000);
        int64_t target = 1 + (check * 13 + call) % 1000000;
        check = (check * 31 + num_subseq(nums, N, (int32_t)target)) % 1000000007;
    }
    printf("200 calls over 100000 values: checksum %lld\n", (long long)check);
    return 0;
}
