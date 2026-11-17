// LeetCode #1182: Maximum Subarray Sum with One Deletion -- the ★ arm in C:
// one pass carrying the best sum ending here with nothing deleted (`kept`)
// and with one element deleted (`cut`).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t maximum_sum(const int64_t *arr, int n) {
    int64_t kept = arr[0];
    int64_t cut = INT64_MIN;
    int64_t best = arr[0];
    for (int i = 1; i < n; i++) {
        int64_t x = arr[i];
        cut = cut == INT64_MIN ? kept : max64(cut + x, kept);
        kept = max64(kept + x, x);
        best = max64(max64(best, kept), cut);
    }
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1182;
    enum { ARRAYS = 10, N = 100000 };
    int64_t *arrays = malloc(sizeof(int64_t) * ARRAYS * N);
    for (int a = 0; a < ARRAYS; a++)
        for (int i = 0; i < N; i++) arrays[a * N + i] = next_random(&seed) % 20001 - 10000;
    int rounds = 100;
    int64_t check = 0;
    for (int r = 0; r < rounds; r++)
        for (int a = 0; a < ARRAYS; a++)
            check = (check * 131 + maximum_sum(arrays + a * N, N) + r) % 1000000007;
    printf("%d rounds of 10 arrays: checksum %lld\n", rounds, (long long)check);
    free(arrays);
    return 0;
}
