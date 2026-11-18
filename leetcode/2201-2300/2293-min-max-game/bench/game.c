// LeetCode #2293: Min Max Game -- the bench, the ★ arm in C. The rounds
// played in place on a copy of the array.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { ARRAYS = 200, N = 1024 };

static int64_t min_max_game(const int64_t *nums, int n, int64_t *a) {
    memcpy(a, nums, sizeof(int64_t) * n);
    while (n > 1) {
        n /= 2;
        for (int i = 0; i < n; i++) {
            int64_t x = a[2 * i], y = a[2 * i + 1];
            a[i] = (i % 2 == 0) == (x < y) ? x : y;
        }
    }
    return a[0];
}

static int64_t seed = 2293;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[ARRAYS][N];
    static int64_t scratch[N];
    for (int k = 0; k < ARRAYS; k++)
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            arrays[k][i] = (hi * 32768 + next_random()) % 1000000000 + 1;
        }
    int64_t check = 0;
    for (int p = 0; p < 50; p++) {
        int64_t total = 0;
        for (int k = 0; k < ARRAYS; k++) total += min_max_game(arrays[k], N, scratch);
        check = (check * 31 + total) % 1000000007;
    }
    printf("50 passes over 200 arrays of 1024: checksum %lld\n", (long long)check);
    return 0;
}
