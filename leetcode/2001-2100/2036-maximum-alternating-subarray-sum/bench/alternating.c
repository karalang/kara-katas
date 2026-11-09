// LeetCode #2036: Maximum Alternating Subarray Sum -- the ★ arm in C, the
// same algorithm and workload as alternating.kara: the best sum ending here
// on a plus, and the one ending on a minus (none yet at the first value,
// a flag for the Option), stepped once per value.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t maximum_alternating_subarray_sum(const int64_t *nums, int n) {
    int64_t plus = nums[0];
    int64_t minus = 0;
    int has_minus = 0;
    int64_t best = plus;
    for (int i = 1; i < n; i++) {
        int64_t x = nums[i];
        int64_t next_plus = has_minus ? max64(x, minus + x) : x;
        minus = plus - x;
        has_minus = 1;
        plus = next_plus;
        best = max64(best, plus);
        best = max64(best, minus);
    }
    return best;
}

static int64_t seed = 2036;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { N = 100000 };
    static int64_t arrays[4][N];
    const int64_t tops[4] = {100000, 1000, 100000, 3};
    for (int a = 0; a < 4; a++) {
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            int64_t lo = next_random();
            arrays[a][i] = (hi * 32768 + lo) % (2 * tops[a] + 1) - tops[a];
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t round = 0; round < 1000; round++) {
        for (int64_t a = 0; a < 4; a++) {
            int64_t at = (round * 7919 + a * 104729) % N;
            arrays[a][at] = -arrays[a][at];
            int64_t answer = maximum_alternating_subarray_sum(arrays[a], N);
            calls++;
            sum += answer;
            check = (check * 31 + answer % 1000000007) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
