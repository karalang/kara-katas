// LeetCode #2064: Minimized Maximum of Products Distributed to Any Store --
// C mirror of the ★ arm's benchmark (stores.kara): 200 problems of 50000
// types, quantities from 1 to 100000, and from 50000 to 100000 stores.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimized_maximum(int64_t n, const int64_t *qs, int64_t m) {
    int64_t lo = 1, hi = 0;
    for (int64_t i = 0; i < m; i++)
        if (qs[i] > hi) hi = qs[i];
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2, need = 0;
        for (int64_t i = 0; i < m; i++) need += (qs[i] + mid - 1) / mid;
        if (need <= n)
            hi = mid;
        else
            lo = mid + 1;
    }
    return lo;
}

static int64_t seed = 2064;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int t = 0; t < 200; t++) {
        int64_t *qs = malloc(50000 * sizeof(int64_t));
        for (int i = 0; i < 50000; i++) {
            int64_t hi = next_random();
            qs[i] = (hi * 32768 + next_random()) % 100000 + 1;
        }
        int64_t hi = next_random();
        int64_t n = 50000 + (hi * 32768 + next_random()) % 50001;
        int64_t a = minimized_maximum(n, qs, 50000);
        free(qs);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    printf("200 problems: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
