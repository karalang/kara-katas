// LeetCode #2001: Number of Pairs of Interchangeable Rectangles -- the
// benchmark, the same algorithm as rectangles.kara: a hash map from the
// reduced ratio to its count (open addressing, linear probing).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t w, h, count; int used; } Slot;

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

static uint64_t hash(int64_t w, int64_t h) {
    uint64_t x = (uint64_t)w * 0x9E3779B97F4A7C15ULL ^ (uint64_t)h * 0xC2B2AE3D27D4EB4FULL;
    x ^= x >> 31;
    x *= 0xBF58476D1CE4E5B9ULL;
    return x ^ (x >> 29);
}

static int64_t interchangeable(const int64_t *w, const int64_t *h, int n) {
    size_t cap = 16;
    while (cap < (size_t)n * 2) cap <<= 1;
    Slot *t = calloc(cap, sizeof(Slot));
    int64_t pairs = 0;
    for (int i = 0; i < n; i++) {
        int64_t g = gcd(w[i], h[i]);
        int64_t kw = w[i] / g, kh = h[i] / g;
        size_t j = hash(kw, kh) & (cap - 1);
        while (t[j].used && (t[j].w != kw || t[j].h != kh)) j = (j + 1) & (cap - 1);
        if (!t[j].used) { t[j].used = 1; t[j].w = kw; t[j].h = kh; t[j].count = 0; }
        pairs += t[j].count;
        t[j].count += 1;
    }
    free(t);
    return pairs;
}

static int64_t seed = 2001;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t calls = 0, sum = 0, check = 0;
    static const int64_t pools[4] = {10, 100, 1000, 10000};
    int64_t *bw = malloc(sizeof(int64_t) * 10000), *bh = malloc(sizeof(int64_t) * 10000);
    int64_t *w = malloc(sizeof(int64_t) * 100000), *h = malloc(sizeof(int64_t) * 100000);
    for (int a = 0; a < 20; a++) {
        int64_t shapes = pools[a % 4];
        for (int64_t i = 0; i < shapes; i++) {
            bw[i] = next_random() % 300 + 1;
            bh[i] = next_random() % 300 + 1;
        }
        for (int i = 0; i < 100000; i++) {
            int64_t b = next_random() % shapes;
            int64_t side = bw[b] > bh[b] ? bw[b] : bh[b];
            int64_t m = next_random() % (100000 / side) + 1;
            w[i] = bw[b] * m;
            h[i] = bh[b] * m;
        }
        for (int r = 0; r < 10; r++) {
            int64_t answer = interchangeable(w, h, 100000);
            sum += answer;
            check = (check * 31 + answer % 1000003) % 1000000007;
            calls++;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    free(bw); free(bh); free(w); free(h);
    return 0;
}
