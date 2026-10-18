// LeetCode 755 — Pour Water, bench: the ★ arm (one drop at a time),
// mirrored from pour_water.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t *pour_water(const int64_t *heights, int64_t n, int64_t volume, int64_t k) {
    int64_t *h = malloc(n * sizeof *h);
    memcpy(h, heights, n * sizeof *h);
    static const int64_t dirs[2] = {-1, 1};
    for (int64_t v = 0; v < volume; v++) {
        int64_t best = k;
        for (int s = 0; s < 2; s++) {
            int64_t d = dirs[s];
            int64_t i = k;
            while (i + d >= 0 && i + d < n && h[i + d] <= h[i]) {
                if (h[i + d] < h[best]) best = i + d;
                i += d;
            }
            if (best != k) break;
        }
        h[best] += 1;
    }
    return h;
}

static int64_t seed = 755;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t rounds = 6000, water = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t heights[100];
        for (int i = 0; i < 100; i++) heights[i] = next_random() % 100;
        int64_t volume = 2000;
        int64_t k = next_random() % 100;
        int64_t *after = pour_water(heights, 100, volume, k);
        for (int i = 0; i < 100; i++) {
            water += after[i];
            check = (check * 31 + after[i]) % 1000000007;
        }
        free(after);
    }
    printf("%lld landscapes of 100 columns, 2000 drops each: %lld units in all, checksum %lld\n", (long long)rounds, (long long)water, (long long)check);
    return 0;
}
