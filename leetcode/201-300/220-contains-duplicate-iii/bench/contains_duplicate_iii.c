#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload for LeetCode #220 — Contains Duplicate III.
 *
 * C has no stdlib hash map, so the bucket-id -> value map is hand-rolled as an
 * open-addressing, linear-probing table with tombstone deletion, shaped to
 * match the runtime's Map[K,V] rather than presized to the workload:
 *
 *   - heap-allocated per call, like the kata's `Map.new()`, and freed after;
 *   - capacity 16 initially, power of two;
 *   - grow (double + full rehash, dropping tombstones) when
 *     (len + tombstones + 1) * 4 > capacity * 3 -- the runtime's exact trigger,
 *     tombstones included;
 *   - insert reuses the first tombstone in the probe chain, matching the
 *     runtime's find_insert_slot;
 *   - FxHash on the key with the same seed the compiler synthesizes (for a
 *     <= 8-byte primitive key that is a single zext + multiply).
 *
 * Counting tombstones in the growth trigger is the load-bearing detail here.
 * This kata is a sliding window: after the first k elements every insert is
 * paired with a remove, so the LIVE size stays at k (<= 543) while tombstones
 * accumulate without bound. The runtime map therefore keeps doubling on a
 * table whose live occupancy never grows -- roughly eleven doublings over the
 * 20 000 operations of a call -- and never shrinks, because resize() only ever
 * goes up.
 *
 * The previous version was a fixed 65 536-entry static table with per-slot
 * generation stamps for an O(1) logical clear. The stamps are a fair trick,
 * but the table was presized past the whole window and so never allocated,
 * grew, or rehashed. Presizing to the answer is not a C advantage, it is a
 * different program -- and here it specifically erased the tombstone-driven
 * growth that dominates the kata's map. */

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

#define BUCKET_EMPTY 0
#define BUCKET_OCCUPIED 1
#define BUCKET_TOMBSTONE 2

typedef struct {
    long *keys;
    long *vals;
    unsigned char *status;
    size_t cap;
    size_t len;
    size_t tombstones;
} Map;

static Map g_map;

static inline unsigned long fxhash_i64(long k) {
    return (unsigned long)k * FXHASH_SEED;
}

static void map_alloc(Map *m, size_t cap) {
    m->cap = cap;
    m->len = 0;
    m->tombstones = 0;
    m->keys = malloc(cap * sizeof(long));
    m->vals = malloc(cap * sizeof(long));
    m->status = calloc(cap, 1); /* BUCKET_EMPTY == 0 */
}

static void map_init(Map *m) { map_alloc(m, INITIAL_CAPACITY); }

static void map_free_storage(Map *m) {
    free(m->keys);
    free(m->vals);
    free(m->status);
}

/* Mirrors find_insert_slot: returns the target slot and whether the key was
 * already present, reusing the first tombstone in the probe chain. */
static size_t map_find_insert_slot(const Map *m, long key, int *exists) {
    size_t mask = m->cap - 1;
    size_t start = (size_t)fxhash_i64(key) & mask;
    size_t first_tomb = (size_t)-1;
    for (size_t i = 0; i < m->cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = m->status[slot];
        if (st == BUCKET_EMPTY) {
            *exists = 0;
            return first_tomb != (size_t)-1 ? first_tomb : slot;
        }
        if (st == BUCKET_TOMBSTONE) {
            if (first_tomb == (size_t)-1) first_tomb = slot;
        } else if (m->keys[slot] == key) {
            *exists = 1;
            return slot;
        }
    }
    *exists = 0;
    return first_tomb != (size_t)-1 ? first_tomb : 0;
}

/* Mirrors resize + rehash_from: double, replay only OCCUPIED slots, drop
 * tombstones. Never shrinks. */
static void map_resize(Map *m) {
    long *ok = m->keys;
    long *ov = m->vals;
    unsigned char *os = m->status;
    size_t ocap = m->cap;

    map_alloc(m, ocap * 2);

    size_t mask = m->cap - 1;
    for (size_t i = 0; i < ocap; i++) {
        if (os[i] != BUCKET_OCCUPIED) continue;
        size_t slot = (size_t)fxhash_i64(ok[i]) & mask;
        while (m->status[slot] != BUCKET_EMPTY) {
            slot = (slot + 1) & mask;
        }
        m->status[slot] = BUCKET_OCCUPIED;
        m->keys[slot] = ok[i];
        m->vals[slot] = ov[i];
        m->len++;
    }
    free(ok);
    free(ov);
    free(os);
}

static void map_insert(Map *m, long key, long val) {
    if ((m->len + m->tombstones + 1) * 4 > m->cap * 3) {
        map_resize(m);
    }
    int exists;
    size_t slot = map_find_insert_slot(m, key, &exists);
    if (!exists) {
        int was_tomb = m->status[slot] == BUCKET_TOMBSTONE;
        m->keys[slot] = key;
        m->len++;
        if (was_tomb) m->tombstones--;
        m->status[slot] = BUCKET_OCCUPIED;
    }
    m->vals[slot] = val;
}

/* Returns 1 and writes *out if present, else 0. */
static int map_get(const Map *m, long key, long *out) {
    size_t mask = m->cap - 1;
    size_t start = (size_t)fxhash_i64(key) & mask;
    for (size_t i = 0; i < m->cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = m->status[slot];
        if (st == BUCKET_EMPTY) return 0;
        if (st == BUCKET_OCCUPIED && m->keys[slot] == key) {
            *out = m->vals[slot];
            return 1;
        }
    }
    return 0;
}

static void map_remove(Map *m, long key) {
    size_t mask = m->cap - 1;
    size_t start = (size_t)fxhash_i64(key) & mask;
    for (size_t i = 0; i < m->cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = m->status[slot];
        if (st == BUCKET_EMPTY) return;
        if (st == BUCKET_OCCUPIED && m->keys[slot] == key) {
            m->status[slot] = BUCKET_TOMBSTONE;
            m->len--;
            m->tombstones++;
            return;
        }
    }
}

static long abs_i64(long x) { return x < 0 ? -x : x; }

static long bucket_of(long x, long w) {
    if (x >= 0) return x / w;
    return (x + 1) / w - 1;
}

static int near_value(long b, long x, long t) {
    long v;
    if (map_get(&g_map, b, &v) && abs_i64(x - v) <= t) return 1;
    return 0;
}

static int contains(const long *nums, long n, long k, long t) {
    if (k <= 0) return 0;
    long w = t + 1;
    map_init(&g_map);
    int found = 0;
    for (long i = 0; i < n; i++) {
        long x = nums[i];
        long b = bucket_of(x, w);
        if (near_value(b, x, t) || near_value(b - 1, x, t) || near_value(b + 1, x, t)) {
            found = 1;
            break;
        }
        map_insert(&g_map, b, x);
        if (i >= k) {
            long old = nums[i - k];
            map_remove(&g_map, bucket_of(old, w));
        }
    }
    map_free_storage(&g_map);
    return found;
}

int main(void) {
    long n = 20000;
    long pairs = 800;
    long valrange = 8000000;
    long half = 4000000;

    long *nums = malloc(n * sizeof(long));
    long state = 12345;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        nums[c] = (state % valrange) - half;
    }

    long sink = 0;
    for (long p = 0; p < pairs; p++) {
        long k = 32 + (p % 512);
        long t = p % 3;
        if (contains(nums, n, k, t)) sink++;
    }
    printf("%ld\n", sink);
    free(nums);
    return 0;
}
