// LeetCode #2811: Check if it is Possible to Split Array -- the bench in
// C: the ★ arm over 100000 arrays of 100 numbers up to 100, m from 150 to
// 200, all drawn first, then each answered 10 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 100000
#define N 100

static int64_t seed = 2811;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int can_split_array(const int64_t *nums, int64_t n, int64_t m) {
    if (n <= 2) return 1;
    for (int64_t i = 1; i < n; i++)
        if (nums[i - 1] + nums[i] >= m) return 1;
    return 0;
}

static int64_t nums_[COUNT][N], ms[COUNT];

int main(void) {
    int rounds = 10;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) nums_[c][i] = next_random() % 100 + 1;
        ms[c] = 150 + next_random() % 51;
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = can_split_array(nums_[c], N, ms[c]);
            yes += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d arrays of 100, %d rounds: %lld can split, checksum %lld\n", COUNT, rounds, (long long)yes, (long long)check);
    return 0;
}
