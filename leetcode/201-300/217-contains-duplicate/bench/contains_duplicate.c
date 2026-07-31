#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload for LeetCode #217 — Contains Duplicate.
 *
 * The kata scans an array once through a hash set, returning true the first time
 * a value repeats. The bench builds ONE big PRNG array, then slides a fixed-width
 * window across it and runs contains_duplicate on every window, counting how many
 * windows contain a duplicate. Each window drives a fresh hash-set membership
 * test whose early-exit is a data-dependent branch (does not vectorize); the load
 * is dominated by hash probing, which is the point — this kata measures the set.
 * Sink = number of windows that contain a duplicate.
 *
 * CROSS-LANGUAGE PARITY (rewritten 2026-07-31). This mirror previously used one
 * STATIC 2048-entry table, presized to >= 2*W so it never grew, and cleared in
 * O(1) between windows by a per-window generation stamp — no allocation, no
 * growth, no rehash, no free, ever. That is a materially cheaper algorithm than
 * the one every other mirror runs, and it made the published comparison
 * meaningless: kara read 19.3x "slower" than this C while simultaneously being
 * FASTER than safety-matched Rust (0.89x). Kara beating Rust but losing 19x to C
 * on a set-probing kernel is the signature of the C mirror doing different work,
 * not the same work faster.
 *
 * The kata's Kara source constructs a FRESH `Set[i64]` per window — 239,200 heap
 * allocations, each growing 16 -> 1024 through ~6 full rehashes, then freed. Rust
 * and Go do the same with their own hash sets. This mirror now does too:
 *
 *   - heap-allocated table per window, freed at the end of it (no static reuse),
 *   - INITIAL_CAPACITY 16, matching runtime/src/map.rs,
 *   - grow at a 3/4 load factor with a full rehash, matching that file's
 *     `(len + tombstones + 1) * 4 > capacity * 3` guard (no tombstones here —
 *     this kata never erases),
 *   - Kara's FxHash finalizer for <=8-byte primitive keys: key * FXHASH_SEED,
 *     the constant in src/codegen/synth.rs. (Set[T] lowers to a Map with
 *     val_size = 0, so it shares Map's capacity and growth policy.)
 *
 * Linear probing rather than the runtime's SIMD control-byte scan: allocation,
 * growth and rehash are what the mismatch was about, and matching the probe
 * sequence exactly would mean reimplementing swisstable in the mirror. */

#define BIG   240000L      /* base array length                     */
#define W     800L         /* window width                          */
#define M     2000000L     /* value range (0..M-1)                  */

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

typedef struct {
    long *keys;
    unsigned char *used;
    unsigned long capacity;
    unsigned long len;
} Set;

static void set_init(Set *s) {
    s->capacity = INITIAL_CAPACITY;
    s->len = 0;
    s->keys = (long *)malloc(s->capacity * sizeof(long));
    s->used = (unsigned char *)calloc(s->capacity, 1);
}

static void set_free(Set *s) {
    free(s->keys);
    free(s->used);
}

static inline unsigned long fxhash(long k) {
    return (unsigned long)((unsigned long long)k * FXHASH_SEED);
}

/* Insert with no growth check — used by the rehash, where capacity is known
 * sufficient and every key is distinct by construction. */
static void set_put_fresh(Set *s, long k) {
    unsigned long h = fxhash(k) & (s->capacity - 1);
    while (s->used[h]) {
        h = (h + 1) & (s->capacity - 1);
    }
    s->used[h] = 1;
    s->keys[h] = k;
    s->len++;
}

static void set_grow(Set *s) {
    unsigned long old_cap = s->capacity;
    long *old_keys = s->keys;
    unsigned char *old_used = s->used;

    s->capacity = old_cap * 2;
    s->len = 0;
    s->keys = (long *)malloc(s->capacity * sizeof(long));
    s->used = (unsigned char *)calloc(s->capacity, 1);

    for (unsigned long i = 0; i < old_cap; i++) {
        if (old_used[i]) {
            set_put_fresh(s, old_keys[i]);
        }
    }
    free(old_keys);
    free(old_used);
}

static int set_contains(const Set *s, long k) {
    unsigned long h = fxhash(k) & (s->capacity - 1);
    while (s->used[h]) {
        if (s->keys[h] == k) return 1;
        h = (h + 1) & (s->capacity - 1);
    }
    return 0;
}

static void set_insert(Set *s, long k) {
    /* runtime/src/map.rs:268 — (len + tombstones + 1) * 4 > capacity * 3 */
    if ((s->len + 1) * 4 > s->capacity * 3) {
        set_grow(s);
    }
    set_put_fresh(s, k);
}

/* returns 1 if the window base[w..w+W] has a repeated value, else 0 */
static int window_has_dup(const long *base, long w) {
    Set seen;
    set_init(&seen);
    for (long t = 0; t < W; t++) {
        long x = base[w + t];
        if (set_contains(&seen, x)) {
            set_free(&seen);
            return 1;                /* already seen => duplicate */
        }
        set_insert(&seen, x);
    }
    set_free(&seen);
    return 0;
}

int main(void) {
    long *base = malloc(BIG * sizeof(long));
    long state = 12345;
    for (long i = 0; i < BIG; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        base[i] = state % M;
    }

    long windows = BIG - W;
    long sink = 0;
    for (long w = 0; w < windows; w++) {
        sink += window_has_dup(base, w);
    }
    printf("%ld\n", sink);
    free(base);
    return 0;
}
