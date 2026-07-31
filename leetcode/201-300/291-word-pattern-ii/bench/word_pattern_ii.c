/* Benchmark harness for LeetCode #291 — Word Pattern II backtracking.
 * Mirrors word_pattern_ii.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map or set, so both are hand-rolled as open-addressing,
 * linear-probing tables with tombstone deletion, shaped to match the runtime's
 * Map[K,V] / Set[T]:
 *
 *   - capacity 16 initially, power of two;
 *   - grow (double + full rehash, dropping tombstones) when
 *     (len + tombstones + 1) * 4 > capacity * 3 -- the runtime's exact trigger,
 *     tombstones included;
 *   - insert reuses the first tombstone in the probe chain, matching the
 *     runtime's find_insert_slot;
 *   - FxHash over the key bytes with the same seed and rotate the compiler
 *     synthesizes (h = rotl(h,5) ^ byte; h *= SEED, from h = 0).
 *
 * This mirror has now been wrong in two opposite directions, and the middle is
 * the correct one.
 *
 * The first revision used open addressing with tombstones but NO resize, so
 * tombstones accumulated with no compaction and probe chains grew without
 * bound -- C became the slowest lane by a wide margin. That was a real defect.
 *
 * The fix was to replace it with a compact association list and a linear scan,
 * on the reasoning that the map never holds more than 3 live entries and
 * unbounded probe growth was "an artifact of the mirror, not a property of C."
 * That reasoning does not hold. The kata allocates ONE map and ONE set for the
 * whole search (`mut ref` parameters, `Map.new()` once in the caller) and
 * inserts and removes at every backtracking step, so the runtime map really
 * does accumulate tombstones and really does keep resizing -- see #220, where
 * the same pattern costs 2.4x. Swapping in a structure with nothing to
 * accumulate did not remove an artifact, it removed the cost every other lane
 * pays.
 *
 * What the first revision actually got wrong was the missing resize. The
 * runtime's trigger counts tombstones and its resize compacts them away, so
 * probe chains stay bounded -- the growth is real but not pathological. This
 * revision restores the hash table with that policy, which is both a faithful
 * mirror and not degenerate.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXSTR 40

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

#define BUCKET_EMPTY 0
#define BUCKET_OCCUPIED 1
#define BUCKET_TOMBSTONE 2

typedef char Str[MAXSTR];

typedef struct {
    Str *key;
    Str *val;
    unsigned char *status;
    size_t cap;
    size_t len;
    size_t tombstones;
} Table;

static unsigned long long fxhash(const char *s) {
    unsigned long long h = 0;
    for (; *s; ++s) {
        h = ((h << 5) | (h >> 59)) ^ (unsigned long long)(unsigned char)*s;
        h *= FXHASH_SEED;
    }
    return h;
}

static void str_copy(char *dst, const char *src) {
    size_t n = strlen(src);
    if (n >= MAXSTR) {
        n = MAXSTR - 1;
    }
    memcpy(dst, src, n);
    dst[n] = '\0';
}

static void tbl_alloc(Table *t, size_t cap) {
    t->cap = cap;
    t->len = 0;
    t->tombstones = 0;
    t->key = malloc(cap * sizeof(Str));
    t->val = malloc(cap * sizeof(Str));
    t->status = calloc(cap, 1); /* BUCKET_EMPTY == 0 */
}

static void tbl_init(Table *t) { tbl_alloc(t, INITIAL_CAPACITY); }

static void tbl_free(Table *t) {
    free(t->key);
    free(t->val);
    free(t->status);
}

/* Mirrors find_insert_slot: target slot plus whether the key was already
 * present, reusing the first tombstone in the probe chain. */
static size_t tbl_insert_slot(const Table *t, const char *key, int *exists) {
    size_t mask = t->cap - 1;
    size_t start = (size_t)fxhash(key) & mask;
    size_t first_tomb = (size_t)-1;
    for (size_t i = 0; i < t->cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = t->status[slot];
        if (st == BUCKET_EMPTY) {
            *exists = 0;
            return first_tomb != (size_t)-1 ? first_tomb : slot;
        }
        if (st == BUCKET_TOMBSTONE) {
            if (first_tomb == (size_t)-1) first_tomb = slot;
        } else if (strcmp(t->key[slot], key) == 0) {
            *exists = 1;
            return slot;
        }
    }
    *exists = 0;
    return first_tomb != (size_t)-1 ? first_tomb : 0;
}

/* Mirrors resize + rehash_from: double, replay only OCCUPIED slots, drop
 * tombstones. Never shrinks. */
static void tbl_resize(Table *t) {
    Str *ok = t->key;
    Str *ov = t->val;
    unsigned char *os = t->status;
    size_t ocap = t->cap;

    tbl_alloc(t, ocap * 2);

    size_t mask = t->cap - 1;
    for (size_t i = 0; i < ocap; i++) {
        if (os[i] != BUCKET_OCCUPIED) continue;
        size_t slot = (size_t)fxhash(ok[i]) & mask;
        while (t->status[slot] != BUCKET_EMPTY) {
            slot = (slot + 1) & mask;
        }
        t->status[slot] = BUCKET_OCCUPIED;
        memcpy(t->key[slot], ok[i], MAXSTR);
        memcpy(t->val[slot], ov[i], MAXSTR);
        t->len++;
    }
    free(ok);
    free(ov);
    free(os);
}

static const char *map_get(const Table *t, const char *key) {
    size_t mask = t->cap - 1;
    size_t start = (size_t)fxhash(key) & mask;
    for (size_t i = 0; i < t->cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = t->status[slot];
        if (st == BUCKET_EMPTY) return 0;
        if (st == BUCKET_OCCUPIED && strcmp(t->key[slot], key) == 0) {
            return t->val[slot];
        }
    }
    return 0;
}

static void map_put(Table *t, const char *key, const char *val) {
    if ((t->len + t->tombstones + 1) * 4 > t->cap * 3) {
        tbl_resize(t);
    }
    int exists;
    size_t slot = tbl_insert_slot(t, key, &exists);
    if (!exists) {
        if (t->status[slot] == BUCKET_TOMBSTONE) t->tombstones--;
        t->status[slot] = BUCKET_OCCUPIED;
        str_copy(t->key[slot], key);
        t->len++;
    }
    str_copy(t->val[slot], val);
}

static void map_del(Table *t, const char *key) {
    size_t mask = t->cap - 1;
    size_t start = (size_t)fxhash(key) & mask;
    for (size_t i = 0; i < t->cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = t->status[slot];
        if (st == BUCKET_EMPTY) return;
        if (st == BUCKET_OCCUPIED && strcmp(t->key[slot], key) == 0) {
            t->status[slot] = BUCKET_TOMBSTONE;
            t->len--;
            t->tombstones++;
            return;
        }
    }
}

static int set_has(const Table *t, const char *key) { return map_get(t, key) != 0; }

#define NP 8
#define SL 30
#define ITERS 500

static int matches(const char *p, size_t pi, size_t plen, const char *s, size_t si, size_t slen,
                   Table *m, Table *used) {
    if (pi >= plen) {
        return si >= slen;
    }
    if (si >= slen) {
        return 0;
    }

    Str key;
    key[0] = p[pi];
    key[1] = '\0';

    const char *bound = map_get(m, key);
    if (bound) {
        Str b;
        str_copy(b, bound); /* copy: map_put below may move it */
        size_t blen = strlen(b);
        if (si + blen > slen) {
            return 0;
        }
        if (strncmp(s + si, b, blen) != 0) {
            return 0;
        }
        return matches(p, pi + 1, plen, s, si + blen, slen, m, used);
    }

    for (size_t end = si + 1; end <= slen; end++) {
        Str cand;
        size_t clen = end - si;
        memcpy(cand, s + si, clen);
        cand[clen] = '\0';
        if (!set_has(used, cand)) {
            map_put(m, key, cand);
            map_put(used, cand, cand);
            if (matches(p, pi + 1, plen, s, end, slen, m, used)) {
                return 1;
            }
            map_del(m, key);
            map_del(used, cand);
        }
    }
    return 0;
}

static int word_pattern_match(const char *p, const char *s) {
    Table m, used;
    tbl_init(&m);
    tbl_init(&used);
    int r = matches(p, 0, strlen(p), s, 0, strlen(s), &m, &used);
    tbl_free(&m);
    tbl_free(&used);
    return r;
}

int main(void) {
    const char *alpha[4] = {"a", "b", "c", "d"};
    static Str subjects[NP];
    for (int j = 0; j < NP; j++) {
        for (int k = 0; k < SL; k++) {
            int kk = (j % 2 == 0) ? (k % (SL / 2)) : k;
            subjects[j][k] = alpha[(kk * 7 + j * 3) % 4][0];
        }
        subjects[j][SL] = '\0';
    }

    const char *pat = "abcabc";
    long long sink = 0;
    for (int it = 0; it < ITERS; it++) {
        int idx = (it * 5) % NP;
        if (word_pattern_match(pat, subjects[idx])) {
            sink += (long long)it + 1;
        } else {
            sink += 1;
        }
    }
    printf("%lld\n", sink);
    return 0;
}
