// Benchmark for #356 -- same workload and algorithm as line_reflection.kara.
// C has no hash set, so is_reflected builds an open-addressing one per call
// (linear probing, splitmix64 over the packed pair), as the other languages
// build their standard set per call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t x, y; } point;

static uint64_t mix(int64_t x, int64_t y) {
    uint64_t z = (uint64_t)x * 0x9E3779B97F4A7C15ULL ^ (uint64_t)y;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

static int is_reflected(const point *pts, size_t n) {
    if (n == 0) return 1;
    size_t cap = 16;
    while (cap < 2 * n) cap <<= 1;
    point *slots = malloc(cap * sizeof(point));
    unsigned char *used = calloc(cap, 1);
    int64_t lo = pts[0].x, hi = pts[0].x;
    for (size_t i = 0; i < n; i++) {
        if (pts[i].x < lo) lo = pts[i].x;
        if (pts[i].x > hi) hi = pts[i].x;
        size_t h = mix(pts[i].x, pts[i].y) & (cap - 1);
        while (used[h] && !(slots[h].x == pts[i].x && slots[h].y == pts[i].y))
            h = (h + 1) & (cap - 1);
        used[h] = 1;
        slots[h] = pts[i];
    }
    int64_t sum = lo + hi;
    int ok = 1;
    for (size_t i = 0; i < n && ok; i++) {
        int64_t wx = sum - pts[i].x, wy = pts[i].y;
        size_t h = mix(wx, wy) & (cap - 1);
        int found = 0;
        while (used[h]) {
            if (slots[h].x == wx && slots[h].y == wy) { found = 1; break; }
            h = (h + 1) & (cap - 1);
        }
        if (!found) ok = 0;
    }
    free(slots);
    free(used);
    return ok;
}

int main(void) {
    int64_t seed = 356;
    int yes = 0;
    int64_t checksum = 0;
    point *pts = malloc(5000 * sizeof(point));
    for (int round = 0; round < 400; round++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t center2 = (seed / 16) % 2000001 - 1000000;
        size_t n = 0;
        for (int k = 0; k < 2500; k++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t x = (seed / 16) % 2000001 - 1000000;
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t y = (seed / 65536) % 1000;
            pts[n++] = (point){x, y};
            pts[n++] = (point){center2 - x, y};
        }
        if (round % 3 == 0) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            size_t i = (size_t)((seed / 65536) % (int64_t)n);
            pts[i].x += 1;
        }
        int r = is_reflected(pts, n);
        if (r) yes++;
        checksum = (checksum * 3 + (r ? 1 : 2)) % 1000000007;
    }
    free(pts);
    printf("%d of 400 sets reflect, checksum %lld\n", yes, (long long)checksum);
    return 0;
}
