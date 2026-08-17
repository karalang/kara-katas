/* LeetCode 280 bench mirror — C. Same greedy, same per-round refresh, same
 * positional-hash sink. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 2000000
#define ROUNDS 30
static void wiggle_sort(int64_t *a, int64_t n) {
    for (int64_t i = 1; i < n; i++) {
        if (i % 2 == 1) { if (a[i] < a[i-1]) { int64_t t=a[i]; a[i]=a[i-1]; a[i-1]=t; } }
        else            { if (a[i] > a[i-1]) { int64_t t=a[i]; a[i]=a[i-1]; a[i-1]=t; } }
    }
}
int main(void) {
    int64_t *src = malloc((size_t)N*sizeof(int64_t));
    int64_t *work = malloc((size_t)N*sizeof(int64_t));
    int64_t seed = 20260818;
    for (int64_t i = 0; i < N; i++) { seed = (seed*1103515245LL+12345LL)%2147483648LL; src[i] = seed % 1000003LL; }
    int64_t sink = 0;
    for (int r = 0; r < ROUNDS; r++) {
        memcpy(work, src, (size_t)N*sizeof(int64_t));
        wiggle_sort(work, N);
        int64_t h = 0;
        for (int64_t j = 0; j < N; j++) h = (h*31 + work[j]) % 1000000007LL;
        sink = (sink + h) % 1000000007LL;
    }
    printf("%lld\n", (long long)sink);
    return 0;
}
