// LeetCode #1283 bench, C: the same binary search, workload and checksum
// as smallest_divisor.kara.
#include <stdint.h>
#include <stdio.h>

#define N 50000

static int64_t total(const int32_t *nums, int n, int64_t d) {
    int64_t sum = 0;
    for (int i = 0; i < n; i++) {
        sum += ((int64_t)nums[i] + d - 1) / d;
    }
    return sum;
}

static int32_t smallest_divisor(const int32_t *nums, int n, int32_t threshold) {
    int64_t lo = 1;
    int64_t hi = nums[0];
    for (int i = 1; i < n; i++) {
        if (nums[i] > hi) {
            hi = nums[i];
        }
    }
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (total(nums, n, mid) <= threshold) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return (int32_t)lo;
}

int main(void) {
    static int32_t nums[N];
    int64_t seed = 1283;
    for (int i = 0; i < N; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        nums[i] = (int32_t)(1 + seed % 1000000);
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 150; r++) {
        int64_t threshold = 50000 + (check + r * 7919) % 950001;
        check = (check * 131 + smallest_divisor(nums, N, (int32_t)threshold)) % 1000000007;
    }
    printf("150 rounds over 5 * 10^4 numbers: checksum %lld\n", (long long)check);
    return 0;
}
