// LeetCode #2110: Number of Smooth Descent Periods of a Stock -- the
// benchmark, the same algorithm as descent.kara: the descent run's length
// up to each day, summed.
#include <stdint.h>
#include <stdio.h>

#define N 100000

static int64_t get_descent_periods(const int64_t *prices, int64_t n) {
    int64_t run = 1, total = 1;
    for (int64_t i = 1; i < n; i++) {
        if (prices[i - 1] - prices[i] == 1) run++;
        else run = 1;
        total += run;
    }
    return total;
}

static int64_t seed = 2110;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[20][N];
    for (int a = 0; a < 20; a++) {
        int64_t p = 5000000;
        for (int i = 0; i < N; i++) {
            arrays[a][i] = p;
            if (next_random() % 4 != 0) p = p - 1;
            else p = p + next_random() % 20;
        }
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 10; round++) {
        for (int a = 0; a < 20; a++) {
            arrays[a][round * 9973] += 1;
            int64_t got = get_descent_periods(arrays[a], N);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("200 counts: %lld periods, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
