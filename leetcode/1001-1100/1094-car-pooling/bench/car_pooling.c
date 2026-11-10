// Benchmark: LeetCode #1094 Car Pooling -- the ★ arm, a difference array
// over the stops. Mirrors car_pooling.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int car_pooling(int64_t trips[][3], int n, int64_t capacity) {
    int64_t *change = calloc(1001, sizeof(int64_t));
    for (int i = 0; i < n; i++) {
        change[trips[i][1]] += trips[i][0];
        change[trips[i][2]] -= trips[i][0];
    }
    int64_t aboard = 0;
    for (int s = 0; s < 1001; s++) {
        aboard += change[s];
        if (aboard > capacity) {
            free(change);
            return 0;
        }
    }
    free(change);
    return 1;
}

static int64_t seed = 1094;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t lists[64][1000][3];

int main(void) {
    for (int j = 0; j < 64; j++) {
        for (int i = 0; i < 1000; i++) {
            int64_t n = next_random() % 100 + 1;
            int64_t a = next_random() % 1000;
            int64_t b = a + 1 + next_random() % (1000 - a);
            lists[j][i][0] = n;
            lists[j][i][1] = a;
            lists[j][i][2] = b;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        for (int64_t j = 0; j < 64; j++) {
            int64_t k = (round * 7 + j * 13) % 1000;
            lists[j][k][0] = 1 + (lists[j][k][0] + round) % 100;
            int64_t lo = 1, hi = 100000;
            while (lo < hi) {
                int64_t mid = (lo + hi) / 2;
                if (car_pooling(lists[j], 1000, mid)) hi = mid;
                else lo = mid + 1;
            }
            total += lo;
            check = (check * 31 + lo) % 1000000007;
        }
    }
    printf("100 rounds over 64 lists of 1000 trips: smallest capacities sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
