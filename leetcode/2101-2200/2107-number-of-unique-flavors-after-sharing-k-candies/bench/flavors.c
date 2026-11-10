// LeetCode #2107: Number of Unique Flavors After Sharing K Candies -- the
// benchmark, the same algorithm as flavors.kara: a hash map of the kept
// flavors' counts (open addressing, linear probing), the shared window
// sliding right one candy at a time.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t key, count; int used; } Slot;

static uint64_t hash(int64_t k) {
    uint64_t x = (uint64_t)k * 0x9E3779B97F4A7C15ULL;
    x ^= x >> 31;
    x *= 0xBF58476D1CE4E5B9ULL;
    return x ^ (x >> 29);
}

static Slot *slot(Slot *t, size_t cap, int64_t key) {
    size_t j = hash(key) & (cap - 1);
    while (t[j].used && t[j].key != key) j = (j + 1) & (cap - 1);
    if (!t[j].used) { t[j].used = 1; t[j].key = key; t[j].count = 0; }
    return &t[j];
}

static int64_t share_candies(const int64_t *candies, int64_t n, int64_t k) {
    size_t cap = 16;
    while (cap < (size_t)n * 2) cap <<= 1;
    Slot *t = calloc(cap, sizeof(Slot));
    for (int64_t i = 0; i < n; i++) slot(t, cap, candies[i])->count += 1;
    for (int64_t i = 0; i < k; i++) slot(t, cap, candies[i])->count -= 1;
    int64_t distinct = 0;
    for (size_t j = 0; j < cap; j++) if (t[j].used && t[j].count > 0) distinct++;
    int64_t best = distinct;
    for (int64_t i = k; i < n; i++) {
        Slot *e = slot(t, cap, candies[i]);
        if (--e->count == 0) distinct--;
        e = slot(t, cap, candies[i - k]);
        if (++e->count == 1) distinct++;
        if (distinct > best) best = distinct;
    }
    free(t);
    return best;
}

static int64_t seed = 2107;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *rows = malloc(sizeof(int64_t) * 20 * 100000);
    for (int r = 0; r < 20; r++) {
        int64_t flavors = next_random() % 5000 + 1;
        for (int i = 0; i < 100000; i++) rows[r * 100000 + i] = next_random() % flavors + 1;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 20; r++) {
        for (int q = 0; q < 5; q++) {
            int64_t hi = next_random();
            int64_t k = (hi * 32768 + next_random()) % 100001;
            int64_t got = share_candies(rows + r * 100000, 100000, k);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("100 shares: %lld flavors kept, checksum %lld\n", (long long)total, (long long)check);
    free(rows);
    return 0;
}
