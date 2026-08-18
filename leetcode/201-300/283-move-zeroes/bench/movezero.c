/* LeetCode 283 bench mirror — C. Same write cursor, same per-round refresh,
 * same position-weighted sink plus write count. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 2000000
#define ROUNDS 60
static void move_zeroes(int64_t *a, int64_t n, int64_t *stores) {
    int64_t write = 0;
    for (int64_t i = 0; i < n; i++)
        if (a[i] != 0) { a[write] = a[i]; (*stores)++; write++; }
    while (write < n) { a[write] = 0; (*stores)++; write++; }
}
int main(void) {
    int64_t *src = malloc((size_t)N*sizeof(int64_t));
    int64_t *work = malloc((size_t)N*sizeof(int64_t));
    int64_t seed = 20260821;
    for (int64_t i = 0; i < N; i++) {
        seed = (seed*1103515245LL+12345LL)%2147483648LL;
        src[i] = (seed % 2 == 0) ? 0 : seed % 100003LL;
    }
    int64_t sink = 0, total = 0;
    for (int r = 0; r < ROUNDS; r++) {
        memcpy(work, src, (size_t)N*sizeof(int64_t));
        int64_t st = 0;
        move_zeroes(work, N, &st);
        total += st;
        int64_t h = 0;
        for (int64_t j = 0; j < N; j++) h = (h*31 + work[j]) % 1000000007LL;
        sink = (sink + h) % 1000000007LL;
    }
    printf("%lld %lld\n", (long long)sink, (long long)total);
    return 0;
}
