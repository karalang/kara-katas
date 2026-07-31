/* Benchmark harness for LeetCode #128 — Longest Consecutive Sequence.
 * Mirrors longest_consecutive.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash set, so one is hand-rolled: open addressing with linear
 * probing over i64 keys. The set is insert-only within a call — this algorithm
 * never deletes — so there are no tombstones and no probe-chain growth (the
 * defect that made #291's first C mirror 3.1x too slow).
 *
 * Deliberately a hash set and NOT a direct-address bitset, even though the
 * values fall in a known 25 000-wide range and a bitset would be far faster.
 * A bitset is a different data structure than the Kara/Rust/Go/Python sets and
 * would make the C column meaningless as a comparison.
 *
 * The table is shaped to match the runtime's Set[T] rather than presized to
 * the workload:
 *
 *   - heap-allocated per call, like the kata's `Set.new()`, and freed on the
 *     way out;
 *   - capacity 16 initially, power of two, linear probing;
 *   - grow (double + full rehash) when (len + 1) * 4 > capacity * 3, i.e. the
 *     same 75% load factor as the runtime map (Set[T] lowers to a Map with a
 *     zero-width value, so it shares that growth policy);
 *   - FxHash on the key with the same seed the compiler synthesizes (for a
 *     <= 8-byte primitive key that is a single zext + multiply).
 *
 * This matters a lot here: 20 000 inserts per call means the kata's set grows
 * 16 -> 32 -> ... -> 65536, twelve doublings and twelve full rehashes, on each
 * of the 150 calls. The previous fixed 65 536-entry static table did none of
 * that -- it was presized to just past the answer and merely memset. Presizing
 * to the answer is not a C advantage, it is a different program.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NP 8
#define N 20000
#define CAPV 25000
#define ITERS 150

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

typedef struct {
    long long *keys;
    unsigned char *used;
    size_t cap;
    size_t len;
} Set;

static inline unsigned long long fxhash_i64(long long k) {
    return (unsigned long long)k * FXHASH_SEED;
}

static void set_init(Set *s) {
    s->cap = INITIAL_CAPACITY;
    s->len = 0;
    s->keys = (long long *)malloc(s->cap * sizeof(long long));
    s->used = (unsigned char *)calloc(s->cap, 1);
}

static void set_free(Set *s) {
    free(s->keys);
    free(s->used);
}

static size_t slot_for(const Set *s, long long k) {
    size_t mask = s->cap - 1;
    size_t h = (size_t)fxhash_i64(k) & mask;
    while (s->used[h] && s->keys[h] != k) {
        h = (h + 1) & mask;
    }
    return h;
}

static void set_grow(Set *s) {
    long long *ok = s->keys;
    unsigned char *ou = s->used;
    size_t ocap = s->cap;

    s->cap = ocap * 2;
    s->keys = (long long *)malloc(s->cap * sizeof(long long));
    s->used = (unsigned char *)calloc(s->cap, 1);

    for (size_t i = 0; i < ocap; i++) {
        if (ou[i]) {
            size_t h = slot_for(s, ok[i]);
            s->used[h] = 1;
            s->keys[h] = ok[i];
        }
    }
    free(ok);
    free(ou);
}

static void set_insert(Set *s, long long k) {
    size_t h = slot_for(s, k);
    if (s->used[h]) {
        return;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((s->len + 1) * 4 > s->cap * 3) {
        set_grow(s);
        h = slot_for(s, k);
    }
    s->used[h] = 1;
    s->keys[h] = k;
    s->len++;
}

static int set_has(const Set *s, long long k) { return s->used[slot_for(s, k)]; }

static long long longest_consecutive(const long long *nums, long long len) {
    Set s;
    set_init(&s);
    for (long long i = 0; i < len; i++) {
        set_insert(&s, nums[i]);
    }
    long long best = 0;
    for (long long i = 0; i < len; i++) {
        long long v = nums[i];
        if (!set_has(&s, v - 1)) {
            long long length = 1;
            long long cur = v;
            while (set_has(&s, cur + 1)) {
                cur++;
                length++;
            }
            if (length > best) {
                best = length;
            }
        }
    }
    set_free(&s);
    return best;
}

static long long arrays[NP][N];

static void lcg(long long seed, long long n, long long cap, long long *out) {
    long long x = seed;
    for (long long k = 0; k < n; k++) {
        x = (x * 1103515245 + 12345) % 2147483648LL;
        out[k] = x % cap;
    }
}

int main(void) {
    for (long long j = 0; j < NP; j++) {
        lcg(j + 1, N, CAPV, arrays[j]);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink += longest_consecutive(arrays[idx], N);
    }
    printf("%lld\n", sink);
    return 0;
}
