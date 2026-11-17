// LeetCode #2256: Minimum Average Difference -- the benchmark's C mirror
// of average.kara: one pass with the total known, the first index whose
// two rounded-down averages are nearest.
#include <stdint.h>
#include <stdio.h>

#define N 100000

static int64_t nums[N];

static int64_t minimum_average_difference(int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    int64_t left = 0, best = 0, best_gap = -1;
    for (int64_t i = 0; i < n; i++) {
        left += nums[i];
        int64_t right = total - left;
        int64_t left_average = left / (i + 1);
        int64_t right_average = i + 1 == n ? 0 : right / (n - i - 1);
        int64_t gap = left_average - right_average;
        if (gap < 0) gap = -gap;
        if (best_gap < 0 || gap < best_gap) {
            best_gap = gap;
            best = i;
        }
    }
    return best;
}

static int64_t seed = 2256;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 20; t++) {
        for (int i = 0; i < N; i++) nums[i] = wide_random() % 100001;
        check = (check * 31 + minimum_average_difference(N) + 1) % 1000000007;
    }
    printf("20 cases of 10^5 values: checksum %lld\n", (long long)check);
    return 0;
}
