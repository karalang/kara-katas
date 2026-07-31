/* Benchmark workload — substring-with-concatenation, LeetCode #30 (sliding window).
 *
 * Algorithmic mirror of concat_words.kara, compiled with `clang -O3`. Same
 * 16-word vocabulary, same glibc LCG (high bits for the vocab pick), same
 * NSLOTS / RUNS, same O(n) sliding-window search, same sink.
 *
 * C has no stdlib hash map, so `need`/`seen` are hand-rolled open-addressing
 * tables keyed on (ptr,len) views into the text — no per-piece allocation,
 * matching the `&str` keys of the Rust mirror and the `string` slices of the
 * Go one. The table mirrors Kāra's `Map[K,V]` shape so the comparison measures
 * the same data structure in every language:
 *
 *   - capacity 16 initially, power of two, linear probing;
 *   - grow (double + full rehash) when (len + 1) * 4 > capacity * 3, i.e. the
 *     same 75% load factor as the runtime's map;
 *   - FxHash over the key bytes with the same seed and rotate the compiler
 *     synthesizes (h = rotl(h,5) ^ byte; h *= SEED, from h = 0).
 *
 * An earlier version of this mirror packed each length-4 word into a u32 and
 * linear-scanned a <= 64-entry id array instead of hashing. That is the
 * natural C shape, but it is NOT the same data structure: it skips both the
 * hash and the key comparison every other mirror pays, so it measured a
 * different program. Kata parity requires the map. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FXHASH_SEED 0x517cc1b727220a95ULL
#define INITIAL_CAPACITY 16UL

typedef struct {
    const char *kp;
    size_t klen;
    long long val;
} Ent;

typedef struct {
    Ent *ents;
    unsigned char *used;
    size_t cap;
    size_t len;
} Map;

static inline unsigned long long fxhash(const char *p, size_t n) {
    unsigned long long h = 0;
    for (size_t i = 0; i < n; i++) {
        h = ((h << 5) | (h >> 59)) ^ (unsigned long long)(unsigned char)p[i];
        h *= FXHASH_SEED;
    }
    return h;
}

static inline int key_eq(const Ent *e, const char *p, size_t n) {
    return e->klen == n && memcmp(e->kp, p, n) == 0;
}

static void map_init(Map *m) {
    m->cap = INITIAL_CAPACITY;
    m->len = 0;
    m->ents = (Ent *)malloc(m->cap * sizeof(Ent));
    m->used = (unsigned char *)calloc(m->cap, 1);
}

static void map_free(Map *m) {
    free(m->ents);
    free(m->used);
    m->ents = NULL;
    m->used = NULL;
    m->cap = 0;
    m->len = 0;
}

static void map_clear(Map *m) {
    memset(m->used, 0, m->cap);
    m->len = 0;
}

/* Insert without the load check or the duplicate check — callers guarantee both. */
static void map_put_fresh(Map *m, const char *p, size_t n, long long v) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash(p, n) & mask;
    while (m->used[h]) {
        h = (h + 1) & mask;
    }
    m->used[h] = 1;
    m->ents[h].kp = p;
    m->ents[h].klen = n;
    m->ents[h].val = v;
    m->len++;
}

static void map_grow(Map *m) {
    Ent *old_e = m->ents;
    unsigned char *old_u = m->used;
    size_t old_cap = m->cap;

    m->cap = old_cap * 2;
    m->len = 0;
    m->ents = (Ent *)malloc(m->cap * sizeof(Ent));
    m->used = (unsigned char *)calloc(m->cap, 1);

    for (size_t i = 0; i < old_cap; i++) {
        if (old_u[i]) {
            map_put_fresh(m, old_e[i].kp, old_e[i].klen, old_e[i].val);
        }
    }
    free(old_e);
    free(old_u);
}

/* Returns a pointer to the stored value, or NULL if the key is absent. */
static long long *map_get(Map *m, const char *p, size_t n) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash(p, n) & mask;
    while (m->used[h]) {
        if (key_eq(&m->ents[h], p, n)) {
            return &m->ents[h].val;
        }
        h = (h + 1) & mask;
    }
    return NULL;
}

static void map_insert(Map *m, const char *p, size_t n, long long v) {
    long long *slot = map_get(m, p, n);
    if (slot) {
        *slot = v;
        return;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((m->len + 1) * 4 > m->cap * 3) {
        map_grow(m);
    }
    map_put_fresh(m, p, n, v);
}

typedef struct {
    long long cnt;
    long long sum_idx;
} Res;

static Res find_substring(const char *s, long long n, const char *const *words,
                          const size_t *wlens, int k) {
    Res res = {0, 0};
    if (k == 0)
        return res;
    size_t wl = wlens[0];
    long long total = (long long)wl * k;
    if (wl == 0 || total > n)
        return res;

    Map need;
    map_init(&need);
    for (int i = 0; i < k; i++) {
        long long *slot = map_get(&need, words[i], wlens[i]);
        long long cur = slot ? *slot : 0;
        map_insert(&need, words[i], wlens[i], cur + 1);
    }

    Map seen;
    map_init(&seen);
    for (size_t r = 0; r < wl; r++) {
        map_clear(&seen);
        long long count = 0;
        long long left = (long long)r;
        long long j = (long long)r;
        while (j + (long long)wl <= n) {
            long long *nreq = map_get(&need, s + j, wl);
            if (!nreq) {
                map_clear(&seen);
                count = 0;
                left = j + (long long)wl;
            } else {
                long long req = *nreq;
                long long *sc = map_get(&seen, s + j, wl);
                long long cur = sc ? *sc : 0;
                map_insert(&seen, s + j, wl, cur + 1);
                count++;
                for (;;) {
                    long long *c2 = map_get(&seen, s + j, wl);
                    if ((c2 ? *c2 : 0) <= req)
                        break;
                    long long *lc = map_get(&seen, s + left, wl);
                    map_insert(&seen, s + left, wl, (lc ? *lc : 0) - 1);
                    left += (long long)wl;
                    count--;
                }
                if (count == k) {
                    res.cnt++;
                    res.sum_idx += left;
                    long long *lc = map_get(&seen, s + left, wl);
                    map_insert(&seen, s + left, wl, (lc ? *lc : 0) - 1);
                    left += (long long)wl;
                    count--;
                }
            }
            j += (long long)wl;
        }
    }
    map_free(&seen);
    map_free(&need);
    return res;
}

int main(void) {
    const long long nslots = 50000;
    const long long runs = 40;

    const char *chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/";

    long long n = nslots * 4;
    char *s = (char *)malloc((size_t)n + 1);
    long long state = 1;
    for (long long t = 0; t < nslots; t++) {
        state = (state * 1103515245LL + 12345) % 2147483648LL;
        long long v = (state / 131072) % 16;
        memcpy(s + t * 4, chars + v * 4, 4);
    }
    s[n] = '\0';

    long long sink = 0;
    for (long long run = 0; run < runs; run++) {
        long long start = run % 13;
        const char *words[4];
        size_t wlens[4];
        for (int d = 0; d < 4; d++) {
            words[d] = chars + (start + d) * 4;
            wlens[d] = 4;
        }
        Res res = find_substring(s, n, words, wlens, 4);
        sink += res.cnt;
        sink += res.sum_idx;
    }

    printf("%lld\n", sink);
    free(s);
    return 0;
}
