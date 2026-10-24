// Benchmark: LeetCode #974 Subarray Sums Divisible by K -- the ★ arm,
// counts of prefix remainders, on 20 arrays of 30000 random numbers.
// Mirrors subarrays_div_by_k.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t subarrays_div_by_k(const int64_t *nums, int64_t n, int64_t k) {
    int64_t *count = calloc((size_t)k, sizeof(int64_t));
    count[0] = 1;
    int64_t sum = 0, total = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        int64_t r = (sum % k + k) % k;
        total += count[r];
        count[r] += 1;
    }
    free(count);
    return total;
}

static int64_t seed = 974;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

#define N 30000
#define COUNT 20

static int64_t nums[COUNT][N];
static int64_t ks[COUNT];

int main(void) {
    int64_t rounds = 200;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) nums[c][i] = next_random() % 20001 - 10000;
        ks[c] = 2 + next_random() % 9999;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t c = (r + i) % COUNT;
            int64_t got = subarrays_div_by_k(nums[c], N, ks[c]);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("%lld rounds over %d arrays of 30000 numbers: %lld subarrays, checksum %lld\n",
           (long long)rounds, COUNT, (long long)total, (long long)check);
    return 0;
}
