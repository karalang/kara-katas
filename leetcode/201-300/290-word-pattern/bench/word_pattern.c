/* Benchmark harness for LeetCode #290 — Word Pattern.
 * Mirrors word_pattern.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map, so both directions of the bijection are hand-rolled
 * as open-addressing tables (linear probing; FNV-1a + strcmp for the
 * word-keyed one, Kara's FxHash finalizer for the letter-keyed one).
 * Word Pattern never deletes, so there are no tombstones and no probe-chain
 * growth from erasure.
 *
 * Deliberately avoids the two traps that made #291's first C mirror 3.1x too
 * slow: string copies use memcpy (not snprintf), and lengths are computed once
 * rather than per call.
 *
 * CROSS-LANGUAGE PARITY (rewritten 2026-07-31). The previous version of this
 * mirror was not the same algorithm as the Kara source, in two ways:
 *
 *   1. `p2w` was a 128-entry array indexed DIRECTLY by letter code — `val[c]`,
 *      no hashing at all. The Kara source uses `Map[i64, String]`.
 *   2. Both tables were `static`, reused across all 2500 iterations and cleared
 *      with a memset of the used-flags. No allocation, no growth, no rehash,
 *      no free, ever — and `w2p` was presized to 4096 so it could not grow.
 *      The Kara source constructs BOTH maps fresh per call, each starting at
 *      capacity 16 and growing by full rehash.
 *
 * That is a materially cheaper algorithm, and the published row showed it:
 * 7.70x "slower" than this C while only 1.46x off safety-matched Rust, which
 * uses real HashMaps like Kara does. This mirror now matches the Kara semantics:
 *
 *   - both maps heap-allocated per call and freed at the end of it,
 *   - INITIAL_CAPACITY 16, per runtime/src/map.rs,
 *   - growth at the same `(len + tombstones + 1) * 4 > capacity * 3` guard
 *     (map.rs:268) with a full rehash,
 *   - the i64-keyed map HASHES its key with Kara's FxHash finalizer
 *     (key * FXHASH_SEED, src/codegen/synth.rs) rather than direct-indexing,
 *   - the String-keyed map stores an owned copy of the key, matching Kara's
 *     deep-copy-on-fresh-insert.
 *
 * FNV-1a is kept for the string hash: the mismatch this rewrite addresses is
 * allocation, growth and direct-indexing, not the choice of string hash, and
 * matching Kara's string hashing exactly would mean reimplementing it here.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NP 8
#define PL 1000
#define ALPHA_N 26
#define ITERS 2500

#define MAXWORD 8
#define SUBLEN (PL * (MAXWORD + 1) + 4)

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

typedef char Word[MAXWORD];

/* ---- letter code -> word (Kara: Map[i64, String]) ---------------------- */

typedef struct {
    long long *key;
    Word *val;
    unsigned char *used;
    unsigned long capacity;
    unsigned long len;
} P2W;

static void p2w_init(P2W *t) {
    t->capacity = INITIAL_CAPACITY;
    t->len = 0;
    t->key = (long long *)malloc(t->capacity * sizeof(long long));
    t->val = (Word *)malloc(t->capacity * sizeof(Word));
    t->used = (unsigned char *)calloc(t->capacity, 1);
}

static void p2w_free(P2W *t) {
    free(t->key);
    free(t->val);
    free(t->used);
}

static inline unsigned long fxhash(long long k) {
    return (unsigned long)((unsigned long long)k * FXHASH_SEED);
}

static unsigned long p2w_slot(const P2W *t, long long k) {
    unsigned long h = fxhash(k) & (t->capacity - 1);
    while (t->used[h] && t->key[h] != k) {
        h = (h + 1) & (t->capacity - 1);
    }
    return h;
}

static void p2w_grow(P2W *t) {
    unsigned long old_cap = t->capacity;
    long long *ok = t->key;
    Word *ov = t->val;
    unsigned char *ou = t->used;

    t->capacity = old_cap * 2;
    t->len = 0;
    t->key = (long long *)malloc(t->capacity * sizeof(long long));
    t->val = (Word *)malloc(t->capacity * sizeof(Word));
    t->used = (unsigned char *)calloc(t->capacity, 1);

    for (unsigned long i = 0; i < old_cap; i++) {
        if (ou[i]) {
            unsigned long h = p2w_slot(t, ok[i]);
            t->used[h] = 1;
            t->key[h] = ok[i];
            memcpy(t->val[h], ov[i], MAXWORD);
            t->len++;
        }
    }
    free(ok);
    free(ov);
    free(ou);
}

/* ---- word -> letter code (Kara: Map[String, i64]) ---------------------- */

typedef struct {
    Word *key;
    long long *val;
    unsigned char *used;
    unsigned long capacity;
    unsigned long len;
} W2P;

static void w2p_init(W2P *t) {
    t->capacity = INITIAL_CAPACITY;
    t->len = 0;
    t->key = (Word *)malloc(t->capacity * sizeof(Word));
    t->val = (long long *)malloc(t->capacity * sizeof(long long));
    t->used = (unsigned char *)calloc(t->capacity, 1);
}

static void w2p_free(W2P *t) {
    free(t->key);
    free(t->val);
    free(t->used);
}

static size_t hash_word(const char *s) {
    size_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h ^= (unsigned char)*s;
        h *= 1099511628211ULL;
    }
    return h;
}

static unsigned long w2p_slot(const W2P *t, const char *key) {
    unsigned long h = (unsigned long)hash_word(key) & (t->capacity - 1);
    while (t->used[h] && strcmp(t->key[h], key) != 0) {
        h = (h + 1) & (t->capacity - 1);
    }
    return h;
}

static void w2p_grow(W2P *t) {
    unsigned long old_cap = t->capacity;
    Word *ok = t->key;
    long long *ov = t->val;
    unsigned char *ou = t->used;

    t->capacity = old_cap * 2;
    t->len = 0;
    t->key = (Word *)malloc(t->capacity * sizeof(Word));
    t->val = (long long *)malloc(t->capacity * sizeof(long long));
    t->used = (unsigned char *)calloc(t->capacity, 1);

    for (unsigned long i = 0; i < old_cap; i++) {
        if (ou[i]) {
            unsigned long h = w2p_slot(t, ok[i]);
            t->used[h] = 1;
            memcpy(t->key[h], ok[i], MAXWORD);
            t->val[h] = ov[i];
            t->len++;
        }
    }
    free(ok);
    free(ov);
    free(ou);
}

/* ----------------------------------------------------------------------- */

static char words[PL][MAXWORD];
static int nwords;

static void split_words(const char *s, size_t slen) {
    nwords = 0;
    size_t cur = 0;
    int have = 0;
    for (size_t i = 0; i < slen; i++) {
        char b = s[i];
        if (b == ' ') {
            if (have) {
                words[nwords][cur] = '\0';
                nwords++;
                cur = 0;
                have = 0;
            }
        } else {
            words[nwords][cur++] = b;
            have = 1;
        }
    }
    if (have) {
        words[nwords][cur] = '\0';
        nwords++;
    }
}

static int word_pattern(const char *pattern, size_t plen, const char *s, size_t slen) {
    split_words(s, slen);
    if (plen != (size_t)nwords) {
        return 0;
    }

    P2W p2w;
    W2P w2p;
    p2w_init(&p2w);
    w2p_init(&w2p);
    int ok = 1;

    for (size_t i = 0; i < plen && ok; i++) {
        long long c = (unsigned char)pattern[i];
        const char *w = words[i];

        unsigned long ph = p2w_slot(&p2w, c);
        if (p2w.used[ph]) {
            if (strcmp(p2w.val[ph], w) != 0) {
                ok = 0;
                break;
            }
        } else {
            /* runtime/src/map.rs:268 — (len + tombstones + 1) * 4 > capacity * 3 */
            if ((p2w.len + 1) * 4 > p2w.capacity * 3) {
                p2w_grow(&p2w);
                ph = p2w_slot(&p2w, c);
            }
            p2w.used[ph] = 1;
            p2w.key[ph] = c;
            memcpy(p2w.val[ph], w, strlen(w) + 1);
            p2w.len++;
        }

        unsigned long h = w2p_slot(&w2p, w);
        if (w2p.used[h]) {
            if (w2p.val[h] != c) {
                ok = 0;
                break;
            }
        } else {
            if ((w2p.len + 1) * 4 > w2p.capacity * 3) {
                w2p_grow(&w2p);
                h = w2p_slot(&w2p, w);
            }
            w2p.used[h] = 1;
            memcpy(w2p.key[h], w, strlen(w) + 1);
            w2p.val[h] = c;
            w2p.len++;
        }
    }

    p2w_free(&p2w);
    w2p_free(&w2p);
    return ok;
}

static char patterns[NP][PL + 1];
static char subjects[NP][SUBLEN];
static size_t sublens[NP];

int main(void) {
    char alpha[ALPHA_N];
    for (int a = 0; a < ALPHA_N; a++) {
        alpha[a] = (char)(97 + a);
    }

    for (int j = 0; j < NP; j++) {
        size_t sp = 0;
        for (int i = 0; i < PL; i++) {
            int slot = (i + j) % ALPHA_N;
            patterns[j][i] = alpha[slot];
            if (i > 0) {
                subjects[j][sp++] = ' ';
            }
            int wslot = slot;
            if (j % 2 == 1 && i == PL - 1) {
                wslot = j % ALPHA_N;
            }
            sp += (size_t)sprintf(subjects[j] + sp, "w%d", wslot);
        }
        patterns[j][PL] = '\0';
        subjects[j][sp] = '\0';
        sublens[j] = sp;
    }

    long long sink = 0;
    for (int it = 0; it < ITERS; it++) {
        int idx = (it * 3) % NP;
        if (word_pattern(patterns[idx], PL, subjects[idx], sublens[idx])) {
            sink += (long long)it + 1;
        } else {
            sink += 1;
        }
    }
    printf("%lld\n", sink);
    return 0;
}
