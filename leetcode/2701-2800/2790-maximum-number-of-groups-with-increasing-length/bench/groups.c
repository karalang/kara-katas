// LeetCode #2790: Maximum Number of Groups With Increasing Length -- the
// bench in C: the ★ arm over 20 arrays of 10^5 limits up to 10^9, all
// drawn first, then each answered 10 times, each answer sorting its own
// copy.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20
#define N 100000

static int64_t seed = 2790;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t copy[N];

static int64_t max_increasing_groups(const int64_t *usage_limits, int64_t n) {
    memcpy(copy, usage_limits, n * sizeof(int64_t));
    qsort(copy, n, sizeof(int64_t), cmp);
    int64_t groups = 0, places = 0;
    for (int64_t i = 0; i < n; i++) {
        places += copy[i];
        if (places >= (groups + 1) * (groups + 2) / 2) groups++;
    }
    return groups;
}

static int64_t cases[COUNT][N];

int main(void) {
    int rounds = 10;
    for (int c = 0; c < COUNT; c++) {
        int64_t top = c % 2 == 0 ? 1000000000 : 100000;
        for (int i = 0; i < N; i++) cases[c][i] = wide() % top + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = max_increasing_groups(cases[c], N);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d arrays of 10^5, %d rounds: groups sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
