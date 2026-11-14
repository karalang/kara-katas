// LeetCode #1560: Most Visited Sector in a Circular Track -- bench: the ★
// arm (the sectors from the first on to the last, wrapping past n) over
// 20000 tracks of up to 100 sectors and 100 legs, built once, each asked
// 100 times.
// C mirror of sectors.kara; each answer is a fresh malloc'd array.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TRACKS 20000

static int64_t *most_visited(int64_t n, const int64_t *rounds, int64_t len, int64_t *count) {
    int64_t start = rounds[0], end = rounds[len - 1];
    int64_t k = 0;
    int64_t *out;
    if (start <= end) {
        out = malloc((end - start + 1) * sizeof(int64_t));
        for (int64_t s = start; s <= end; s++) out[k++] = s;
    } else {
        out = malloc((end + n - start + 1) * sizeof(int64_t));
        for (int64_t s = 1; s <= end; s++) out[k++] = s;
        for (int64_t s = start; s <= n; s++) out[k++] = s;
    }
    *count = k;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1560;
    static int64_t ns[TRACKS], lens[TRACKS];
    static int64_t *tracks[TRACKS];
    for (int t = 0; t < TRACKS; t++) {
        int64_t n = next_random(&seed) % 99 + 2;
        int64_t m = next_random(&seed) % 100 + 1;
        int64_t *rounds = malloc((m + 1) * sizeof(int64_t));
        rounds[0] = next_random(&seed) % n + 1;
        for (int64_t i = 1; i <= m; i++) {
            int64_t at = rounds[i - 1];
            rounds[i] = (at - 1 + next_random(&seed) % (n - 1) + 1) % n + 1;
        }
        ns[t] = n;
        lens[t] = m + 1;
        tracks[t] = rounds;
    }
    int64_t check = 0, total = 0;
    for (int64_t pass = 0; pass < 100; pass++) {
        for (int64_t t = 0; t < TRACKS; t++) {
            int64_t count;
            int64_t *sectors = most_visited(ns[t], tracks[t], lens[t], &count);
            total += count;
            check = mix(check, sectors[(pass * 7 + t) % count]);
            free(sectors);
        }
    }
    printf("100 passes over 20000 tracks: %lld sectors, checksum %lld\n", (long long)total, (long long)check);
    for (int t = 0; t < TRACKS; t++) free(tracks[t]);
    return 0;
}
