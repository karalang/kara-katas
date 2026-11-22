// LeetCode #2778: Sum of Squares of Special Elements -- the bench in C:
// the ★ arm over 100000 random arrays, all drawn first, then each
// answered 20 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 100000

static int64_t seed = 2778;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t sum_of_squares(const int64_t *nums, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 1; i <= n; i++) {
        if (n % i == 0) total += nums[i - 1] * nums[i - 1];
    }
    return total;
}

static int64_t arrays[COUNT][50], lengths[COUNT];

int main(void) {
    int rounds = 20;
    for (int c = 0; c < COUNT; c++) {
        lengths[c] = next_random() % 50 + 1;
        for (int64_t i = 0; i < lengths[c]; i++) arrays[c][i] = next_random() % 50 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t s = sum_of_squares(arrays[c], lengths[c]);
            total += s;
            check = (check * 31 + s + r) % 1000000007;
        }
    }
    printf("%d arrays, %d rounds: sums total %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
