// Benchmark for #410: mirror of split_array.kara (binary search on the
// answer).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t pieces_needed(const int64_t *nums, int64_t n, int64_t cap) {
    int64_t pieces = 1, sum = 0;
    for (int64_t i = 0; i < n; i++) {
        if (sum + nums[i] > cap) {
            pieces++;
            sum = nums[i];
        } else {
            sum += nums[i];
        }
    }
    return pieces;
}

static int64_t split_array(const int64_t *nums, int64_t n, int64_t k) {
    int64_t lo = 0, hi = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] > lo) {
            lo = nums[i];
        }
        hi += nums[i];
    }
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (pieces_needed(nums, n, mid) <= k) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t arrays = argc > 1 ? atoll(argv[1]) : 10000;
    int64_t n = 1000, seed = 410, total = 0, checksum = 0;
    int64_t *nums = malloc(n * sizeof *nums);
    for (int64_t t = 0; t < arrays; t++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t hi = step(&seed);
            int64_t lo = step(&seed);
            nums[i] = (hi * 32768 + lo) % 1000001;
        }
        int64_t k = 1 + step(&seed) % 50;
        int64_t answer = split_array(nums, n, k);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld arrays of %lld numbers: total %lld, checksum %lld\n", (long long)arrays, (long long)n, (long long)total, (long long)checksum);
    free(nums);
    return 0;
}
