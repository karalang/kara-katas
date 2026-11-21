// LeetCode #2527: Find Xor-Beauty of Array -- C mirror of the benchmark
// (xor.kara): the same lists, passes, order and checksum.
#include <stdint.h>
#include <stdio.h>

static int64_t xor_beauty(const int64_t *nums, int n) {
    int64_t beauty = 0;
    for (int i = 0; i < n; i++) beauty ^= nums[i];
    return beauty;
}

static int64_t seed = 2527;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

static int64_t lists[1000][100];

int main(void) {
    for (int t = 0; t < 1000; t++)
        for (int j = 0; j < 100; j++) lists[t][j] = wide_random() % 1000000000 + 1;
    const int passes = 3000;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        int64_t start = check % 1000;
        for (int64_t i = 0; i < 1000; i++)
            check = (check * 31 + xor_beauty(lists[(start + i) % 1000], 100) + p) % 1000000007;
    }
    printf("%d passes over 1000 lists of 100 numbers: checksum %lld\n", passes, (long long)check);
    return 0;
}
