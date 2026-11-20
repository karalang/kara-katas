// LeetCode #1746: Maximum Subarray Sum After One Operation -- the bench
// (square.kara in C): Kadane's scan with two states.
#include <stdint.h>
#include <stdio.h>

enum { COUNT = 20, ROUNDS = 40, N = 100000 };

static int32_t max32(int32_t a, int32_t b) { return a > b ? a : b; }

static int32_t max_sum_after_operation(const int32_t *nums, int64_t n) {
    int32_t plain = 0, squared = 0, best = INT32_MIN;
    for (int64_t i = 0; i < n; i++) {
        int32_t x = nums[i];
        squared = max32(squared + x, max32(plain, 0) + x * x);
        plain = max32(plain, 0) + x;
        best = max32(best, squared);
    }
    return best;
}

static int64_t seed = 1746;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t arrays[COUNT][N];
    for (int c = 0; c < COUNT; c++)
        for (int64_t i = 0; i < N; i++) arrays[c][i] = (int32_t)(next_random() % 20001 - 10000);
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = max_sum_after_operation(arrays[c], N);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: sums add to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)sum, (long long)check);
    return 0;
}
