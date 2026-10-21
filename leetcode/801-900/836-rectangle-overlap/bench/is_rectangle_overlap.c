// Benchmark for #836: Rectangle Overlap -- the ★ arm (the two projections).
//
// Mirrors is_rectangle_overlap.kara: two axis-aligned rectangles overlap
// with positive area exactly when their shadows on the x axis overlap in
// more than a point and so do their shadows on the y axis.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }
static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static bool is_rectangle_overlap(const int64_t rec1[4], const int64_t rec2[4]) {
    int64_t left = max64(rec1[0], rec2[0]);
    int64_t right = min64(rec1[2], rec2[2]);
    int64_t bottom = max64(rec1[1], rec2[1]);
    int64_t top = min64(rec1[3], rec2[3]);
    return left < right && bottom < top;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

// a number below 2^32, from three draws
static int64_t big_random(int64_t *seed) {
    int64_t hi = next_random(seed) * 32768;
    hi += next_random(seed);
    return hi * 4 + next_random(seed) % 4;
}

int main(void) {
    // 4096 rectangles drawn once in LeetCode's range, their corners
    // anywhere and their sides up to 2 * 10^9 >> (k % 8) for rectangle k,
    // so they run from the size of the range down to a 128th of it.
    // Round s tests each rectangle i against rectangle (i + s + 1) % 4096.
    enum { N = 4096 };
    const int64_t n = N, rounds = 100000;
    int64_t seed = 836;
    static int64_t rects[N][4];
    for (int64_t k = 0; k < n; k++) {
        int64_t reach = (int64_t)2000000000 >> (k % 8);
        int64_t x1 = big_random(&seed) % 2000000000 - 1000000000;
        int64_t y1 = big_random(&seed) % 2000000000 - 1000000000;
        int64_t x2 = min64(x1 + 1 + big_random(&seed) % reach, 1000000000);
        int64_t y2 = min64(y1 + 1 + big_random(&seed) % reach, 1000000000);
        rects[k][0] = x1;
        rects[k][1] = y1;
        rects[k][2] = x2;
        rects[k][3] = y2;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t s = 0; s < rounds; s++) {
        int64_t overlapping = 0;
        for (int64_t i = 0; i < n; i++)
            if (is_rectangle_overlap(rects[i], rects[(i + s + 1) % n])) overlapping += 1;
        total += overlapping;
        checksum = (checksum * 131 + overlapping) % 1000000007;
    }
    printf("%lld rounds of %lld pairs: %lld overlapping, checksum %lld\n", (long long)rounds, (long long)n,
           (long long)total, (long long)checksum);
    return 0;
}
