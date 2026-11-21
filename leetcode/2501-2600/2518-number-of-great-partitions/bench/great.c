// LeetCode #2518: Number of Great Partitions -- C mirror of the benchmark
// (great.kara): the same lists, passes, order and checksum.
#include <stdint.h>
#include <stdio.h>

#define MOD 1000000007LL

static int64_t lists[20][1000];
static int64_t ways[1000];

static int64_t count_partitions(const int64_t *nums, int64_t n, int64_t k) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    if (total < 2 * k) return 0;
    for (int64_t s = 0; s < k; s++) ways[s] = 0;
    ways[0] = 1;
    int64_t all = 1;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        all = all * 2 % MOD;
        if (x < k)
            for (int64_t s = k - 1; s >= x; s--) ways[s] = (ways[s] + ways[s - x]) % MOD;
    }
    int64_t shortfall = 0;
    for (int64_t s = 0; s < k; s++) shortfall = (shortfall + ways[s]) % MOD;
    return ((all - 2 * shortfall) % MOD + MOD) % MOD;
}

static int64_t seed = 2518;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    for (int t = 0; t < 20; t++)
        for (int i = 0; i < 1000; i++) lists[t][i] = next_random() % 1000 + 1;
    const int64_t passes = 35;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++)
        for (int t = 0; t < 20; t++)
            check = (check * 31 + count_partitions(lists[t], 1000, check % 1000 + 1) + p) % MOD;
    printf("%lld passes over 20 lists of 1000 numbers: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
