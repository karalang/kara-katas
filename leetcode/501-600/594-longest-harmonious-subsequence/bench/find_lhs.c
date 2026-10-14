// Benchmark for #594: C mirror of the ★ arm (count in a hash table, then
// pair); see find_lhs.kara. C has no map, so this is an open-addressing
// table by hand, sized to a power of two at least twice the input,
// hashed with the splitmix64 finalizer and allocated per call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t key, count;
    int used;
} Slot;

static uint64_t mix(uint64_t x) {
    x ^= x >> 30;
    x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27;
    x *= 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

static Slot *find(Slot *t, uint64_t mask, int64_t key) {
    uint64_t i = mix((uint64_t)key) & mask;
    while (t[i].used && t[i].key != key)
        i = (i + 1) & mask;
    return &t[i];
}

static int64_t find_lhs(const int64_t *nums, int64_t n) {
    uint64_t size = 1;
    while (size < 2 * (uint64_t)n)
        size <<= 1;
    Slot *t = calloc(size, sizeof(Slot));
    for (int64_t k = 0; k < n; k++) {
        Slot *s = find(t, size - 1, nums[k]);
        if (!s->used) {
            s->used = 1;
            s->key = nums[k];
        }
        s->count++;
    }
    int64_t best = 0;
    for (uint64_t i = 0; i < size; i++)
        if (t[i].used) {
            Slot *s = find(t, size - 1, t[i].key + 1);
            if (s->used && t[i].count + s->count > best)
                best = t[i].count + s->count;
        }
    free(t);
    return best;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = step(seed);
    int64_t lo = step(seed);
    return hi * 32768 + lo;
}

int main(void) {
    enum { COUNT = 100, ROUNDS = 20, N = 20000 };
    int64_t seed = 594;
    static int64_t arrays[COUNT][N];
    for (int k = 0; k < COUNT; k++) {
        int64_t range = 1 + wide(&seed) % 5000;
        int64_t low = wide(&seed) % 1999990000 - 999990000;
        for (int j = 0; j < N; j++)
            arrays[k][j] = low + wide(&seed) % range;
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            int64_t got = find_lhs(arrays[(round * 7 + g) % COUNT], N);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    printf("%d arrays, %d rounds: total %lld, checksum %lld\n", COUNT, ROUNDS, (long long)total,
           (long long)checksum);
    return 0;
}
