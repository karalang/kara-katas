// LeetCode #1552: Magnetic Force Between Two Balls -- bench: the ★ arm (a
// binary search on the answer, a greedy check) over 20 baskets of 100000
// distinct positions up to 10^9, built once, each asked 5 times with its own
// number of balls every time. C mirror of magnetic.kara:
// the positions are sorted by qsort, and the distinct draws are kept
// distinct by an open-addressing table built once.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int fits(const int64_t *sorted, int64_t n, int64_t m, int64_t gap) {
    int64_t placed = 1, last = sorted[0];
    for (int64_t i = 0; i < n; i++) {
        if (sorted[i] - last >= gap) {
            placed++;
            last = sorted[i];
        }
    }
    return placed >= m;
}

static int64_t max_distance(const int64_t *position, int64_t n, int64_t m) {
    int64_t *sorted = malloc(n * sizeof(int64_t));
    memcpy(sorted, position, n * sizeof(int64_t));
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t lo = 1, hi = sorted[n - 1] - sorted[0];
    while (lo < hi) {
        int64_t mid = lo + (hi - lo + 1) / 2;
        if (fits(sorted, n, m, mid)) lo = mid;
        else hi = mid - 1;
    }
    free(sorted);
    return lo;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

#define CAP (1 << 18)

int main(void) {
    int64_t seed = 1552;
    static int64_t baskets[20][100000];
    static int64_t table[CAP];
    for (int b = 0; b < 20; b++) {
        memset(table, 0, sizeof table);
        int64_t n = 0;
        while (n < 100000) {
            int64_t p = (next_random(&seed) * 32768 + next_random(&seed)) % 1000000000 + 1;
            uint64_t h = (uint64_t)p * 0x9E3779B97F4A7C15ull >> 46;
            int fresh = 1;
            while (table[h]) {
                if (table[h] == p) { fresh = 0; break; }
                h = (h + 1) & (CAP - 1);
            }
            if (fresh) {
                table[h] = p;
                baskets[b][n++] = p;
            }
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 5; pass++) {
        for (int64_t b = 0; b < 20; b++) {
            int64_t m = (pass * 20 + b) * 997 % 99999 + 2;
            check = mix(check, max_distance(baskets[b], 100000, m));
        }
    }
    printf("5 passes over 20 baskets of 100000 positions: checksum %lld\n", (long long)check);
    return 0;
}
