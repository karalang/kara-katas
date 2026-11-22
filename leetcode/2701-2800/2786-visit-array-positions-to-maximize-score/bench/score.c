// LeetCode #2786: Visit Array Positions to Maximize Score -- the bench in
// C: the ★ arm over 20 arrays of 10^5 numbers up to 10^6 with x up to
// 10^6, all drawn first, then each answered 100 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 20
#define N 100000

static int64_t seed = 2786;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t max_score(const int64_t *nums, int64_t n, int64_t x) {
    int64_t unreached = -1000000000000000LL;
    int64_t best[2] = {unreached, unreached};
    best[nums[0] % 2] = nums[0];
    for (int64_t i = 1; i < n; i++) {
        int64_t v = nums[i], p = v % 2;
        int64_t a = best[p], b = best[1 - p] - x;
        best[p] = (a > b ? a : b) + v;
    }
    return best[0] > best[1] ? best[0] : best[1];
}

static int64_t cases[COUNT][N], xs[COUNT];

int main(void) {
    int rounds = 100;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) cases[c][i] = wide() % 1000000 + 1;
        xs[c] = wide() % 1000000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = max_score(cases[c], N, xs[c]);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d arrays of 10^5, %d rounds: scores sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
