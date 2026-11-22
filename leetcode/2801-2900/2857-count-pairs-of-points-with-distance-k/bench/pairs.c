// LeetCode #2857: Count Pairs of Points With Distance k -- the bench:
// the ★ arm over 10 cases of 50000 points, LeetCode's most, every
// other one in a 256 x 256 square and the rest up to 10^6, with k up
// to 100, all drawn first, then each answered 3 times.
// C has no map: an open-addressing table of (x, y) keys with a
// splitmix64 hash, cleared for every case.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP (1 << 17)

typedef struct { int64_t x, y, count; int used; } Slot;
static Slot table[CAP];

static uint64_t mix(int64_t x, int64_t y) {
    uint64_t z = (uint64_t)x * 0x9E3779B97F4A7C15ULL ^ (uint64_t)y;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

static Slot *find(int64_t x, int64_t y) {
    uint64_t i = mix(x, y) & (CAP - 1);
    while (table[i].used && (table[i].x != x || table[i].y != y)) i = (i + 1) & (CAP - 1);
    return &table[i];
}

static int64_t count_pairs(const int64_t *xs, const int64_t *ys, int64_t n, int64_t k) {
    memset(table, 0, sizeof(table));
    int64_t pairs = 0;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t a = 0; a <= k; a++) {
            Slot *s = find(xs[i] ^ a, ys[i] ^ (k - a));
            if (s->used) pairs += s->count;
        }
        Slot *s = find(xs[i], ys[i]);
        if (!s->used) {
            s->used = 1;
            s->x = xs[i];
            s->y = ys[i];
            s->count = 0;
        }
        s->count++;
    }
    return pairs;
}

static int64_t seed = 2857;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 10, rounds = 3, n = 50000;
    int64_t *xs = malloc(sizeof(int64_t) * count * n), *ys = malloc(sizeof(int64_t) * count * n);
    int64_t ks[10];
    for (int64_t c = 0; c < count; c++) {
        int64_t top = c % 2 == 0 ? 256 : 1000001;
        ks[c] = next_random() % 101;
        for (int64_t i = 0; i < n; i++) {
            xs[c * n + i] = wide() % top;
            ys[c * n + i] = wide() % top;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t pairs = count_pairs(xs + c * n, ys + c * n, n, ks[c]);
            total += pairs;
            check = (check * 31 + pairs + r) % 1000000007;
        }
    }
    printf("%lld cases of %lld points, %lld rounds: %lld pairs, checksum %lld\n", (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(xs);
    free(ys);
    return 0;
}
