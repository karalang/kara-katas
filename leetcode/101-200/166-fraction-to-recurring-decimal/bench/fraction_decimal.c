#include <stdio.h>
#include <stdlib.h>

/* The kata tracks seen remainders in a `Map[i64, i64]`; C has no stdlib map, so
 * one is hand-rolled here as an open-addressing, linear-probing table shaped to
 * match the runtime's Map[K,V]:
 *
 *   - heap-allocated per pass, like the kata's `Map.new()`, and freed after;
 *   - capacity 16 initially, power of two;
 *   - grow (double + full rehash) when (len + 1) * 4 > capacity * 3, i.e. the
 *     same 75% load factor as the runtime map;
 *   - FxHash on the key with the same seed the compiler synthesizes (for a
 *     <= 8-byte primitive key that is a single zext + multiply).
 *
 * The previous version was a direct-address table -- `seen[rem]` indexed by the
 * remainder itself, with an epoch stamp for an O(1) per-pass clear. The epoch
 * stamp is a fair trick, but direct addressing is not a fast map, it is the
 * absence of one: no hash, no probe, no growth, and it only works because the
 * key range happens to be bounded by the denominator. Every other mirror hashes.
 */

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

typedef struct {
    long *keys;
    long *vals;
    unsigned char *used;
    size_t cap;
    size_t len;
} Map;

static inline unsigned long fxhash_i64(long k) {
    return (unsigned long)k * FXHASH_SEED;
}

static void map_init(Map *m) {
    m->cap = INITIAL_CAPACITY;
    m->len = 0;
    m->keys = malloc(m->cap * sizeof(long));
    m->vals = malloc(m->cap * sizeof(long));
    m->used = calloc(m->cap, 1);
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->vals);
    free(m->used);
}

static size_t map_slot(const Map *m, long k) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash_i64(k) & mask;
    while (m->used[h] && m->keys[h] != k) {
        h = (h + 1) & mask;
    }
    return h;
}

static int map_has(const Map *m, long k) { return m->used[map_slot(m, k)]; }

static void map_grow(Map *m) {
    long *ok = m->keys;
    long *ov = m->vals;
    unsigned char *ou = m->used;
    size_t ocap = m->cap;

    m->cap = ocap * 2;
    m->keys = malloc(m->cap * sizeof(long));
    m->vals = malloc(m->cap * sizeof(long));
    m->used = calloc(m->cap, 1);

    for (size_t i = 0; i < ocap; i++) {
        if (ou[i]) {
            size_t h = map_slot(m, ok[i]);
            m->used[h] = 1;
            m->keys[h] = ok[i];
            m->vals[h] = ov[i];
        }
    }
    free(ok);
    free(ov);
    free(ou);
}

static void map_insert(Map *m, long k, long v) {
    size_t h = map_slot(m, k);
    if (m->used[h]) {
        m->vals[h] = v;
        return;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((m->len + 1) * 4 > m->cap * 3) {
        map_grow(m);
        h = map_slot(m, k);
    }
    m->used[h] = 1;
    m->keys[h] = k;
    m->vals[h] = v;
    m->len++;
}

static long frac_checksum(long num, long den) {
    long rem = num % den;
    long checksum = 0;
    if (rem == 0) return 0;

    Map seen;
    map_init(&seen);
    long count = 0;
    while (rem != 0) {
        if (map_has(&seen, rem)) {
            rem = 0; /* cycle closed — stop */
        } else {
            map_insert(&seen, rem, count);
            rem *= 10;
            long digit = rem / den;
            checksum += digit;
            rem %= den;
            count++;
        }
    }
    map_free(&seen);
    return checksum;
}

int main(void) {
    long passes = 500000;
    long state = 12345, sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long num = state % 1000000;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long den = 2 + (state % 1023);
        sink += frac_checksum(num, den);
    }
    printf("%ld\n", sink);
    return 0;
}
