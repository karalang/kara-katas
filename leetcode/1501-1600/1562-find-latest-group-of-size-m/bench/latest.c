// LeetCode #1562: Find Latest Group of Size M -- bench: the ★ arm (group
// lengths kept at both ends, a count of groups of length m) over 20 random
// orders of 100000 positions, built once, each asked for m from 1 to 10.
// C mirror of latest.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t find_latest_step(const int64_t *arr, int64_t n, int64_t m) {
    int64_t *length = calloc(n + 2, sizeof(int64_t));
    int64_t groups_of_m = 0, latest = -1;
    for (int64_t step = 0; step < n; step++) {
        int64_t a = arr[step];
        int64_t left = length[a - 1], right = length[a + 1];
        int64_t total = left + right + 1;
        if (left == m) groups_of_m--;
        if (right == m) groups_of_m--;
        if (total == m) groups_of_m++;
        length[a - left] = total;
        length[a + right] = total;
        if (groups_of_m > 0) latest = step + 1;
    }
    free(length);
    return latest;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1562;
    static int64_t orders[20][N];
    for (int o = 0; o < 20; o++) {
        for (int64_t i = 0; i < N; i++) orders[o][i] = i + 1;
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t j = next_random(&seed) * 32768;
            j = (j + next_random(&seed)) % (i + 1);
            int64_t t = orders[o][i];
            orders[o][i] = orders[o][j];
            orders[o][j] = t;
        }
    }
    int64_t check = 0, total = 0;
    for (int64_t m = 1; m <= 10; m++) {
        for (int o = 0; o < 20; o++) {
            int64_t step = find_latest_step(orders[o], N, m);
            total += step;
            check = mix(check, step);
        }
    }
    printf("m from 1 to 10 over 20 orders of 100000 positions: steps sum %lld, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
