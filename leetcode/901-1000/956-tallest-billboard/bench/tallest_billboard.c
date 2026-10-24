// LeetCode #956: Tallest Billboard -- C mirror of the Kara bench program
// (the shorter side by difference).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long tallest_billboard(const long *rods, long n) {
    long total = 0;
    for (long i = 0; i < n; i++) {
        total += rods[i];
    }
    long *best = malloc(sizeof(long) * (total + 1));
    long *prev = malloc(sizeof(long) * (total + 1));
    for (long d = 0; d <= total; d++) {
        best[d] = -1;
    }
    best[0] = 0;
    for (long i = 0; i < n; i++) {
        long r = rods[i];
        memcpy(prev, best, sizeof(long) * (total + 1));
        for (long d = 0; d <= total; d++) {
            if (prev[d] < 0) {
                continue;
            }
            long shrt = prev[d];
            if (d + r <= total && shrt > best[d + r]) {
                best[d + r] = shrt;
            }
            long nd = labs(d - r);
            long ns = shrt + (d < r ? d : r);
            if (ns > best[nd]) {
                best[nd] = ns;
            }
        }
    }
    long out = best[0];
    free(best);
    free(prev);
    return out;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    const long rounds = 30, count = 200, n = 20;
    long seed = 956;
    long *sets = malloc(sizeof(long) * count * n);
    for (long s = 0; s < count; s++) {
        for (long i = 0; i < n; i++) {
            sets[s * n + i] = 1 + next_random(&seed) % 250;
        }
    }
    long total = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (long i = 0; i < count; i++) {
            long k = (r + i) % count;
            long h = tallest_billboard(&sets[k * n], n);
            total += h;
            check = (check * 31 + h) % 1000000007;
        }
    }
    printf("%ld rounds over %ld sets of %ld rods up to 250: heights adding to %ld, checksum %ld\n", rounds, count, n, total, check);
    return 0;
}
