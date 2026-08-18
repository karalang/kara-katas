/* Bench mirror for LeetCode #895 — same algorithm as the Kara version.
 *
 * PARITY NOTE. The Kara/Rust/Go/Python mirrors all key their two structures on
 * a hash map, so this one does too: an open-addressing table with linear
 * probing, one for `freq` and one for the per-frequency `buckets`. A
 * direct-address array indexed by value would be faster here — the domain is
 * 0..11 — but it would be a DIFFERENT data structure, and the corpus rule is
 * that every mirror runs the same algorithm. Benchmarking a C array against
 * four hash maps would measure the shortcut, not the compiler. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP 1024 /* power of two; > any live key count in this workload */

typedef struct {
    long key;
    long val;
    int used;
} IEntry;

typedef struct {
    long key;
    long *vec;
    long len, cap;
    int used;
} BEntry;

static size_t hash_idx(long k) { return (size_t)((unsigned long)k * 2654435761u) & (CAP - 1); }

/* long -> long */
static long imap_get(IEntry *t, long k, long dflt) {
    size_t i = hash_idx(k);
    while (t[i].used) {
        if (t[i].key == k) return t[i].val;
        i = (i + 1) & (CAP - 1);
    }
    return dflt;
}

static void imap_put(IEntry *t, long k, long v) {
    size_t i = hash_idx(k);
    while (t[i].used) {
        if (t[i].key == k) { t[i].val = v; return; }
        i = (i + 1) & (CAP - 1);
    }
    t[i].used = 1;
    t[i].key = k;
    t[i].val = v;
}

/* long -> vector<long>, returned by address so the caller appends in place */
static BEntry *bmap_slot(BEntry *t, long k) {
    size_t i = hash_idx(k);
    while (t[i].used) {
        if (t[i].key == k) return &t[i];
        i = (i + 1) & (CAP - 1);
    }
    t[i].used = 1;
    t[i].key = k;
    t[i].vec = NULL;
    t[i].len = 0;
    t[i].cap = 0;
    return &t[i];
}

typedef struct {
    IEntry freq[CAP];
    BEntry buckets[CAP];
    long maxfreq;
} FreqStack;

static void fs_init(FreqStack *s) {
    memset(s->freq, 0, sizeof(s->freq));
    memset(s->buckets, 0, sizeof(s->buckets));
    s->maxfreq = 0;
}

static void fs_free(FreqStack *s) {
    for (int i = 0; i < CAP; i++)
        if (s->buckets[i].used) free(s->buckets[i].vec);
}

static void fs_push(FreqStack *s, long x) {
    long f = imap_get(s->freq, x, 0) + 1;
    imap_put(s->freq, x, f);
    if (f > s->maxfreq) s->maxfreq = f;
    BEntry *b = bmap_slot(s->buckets, f);
    if (b->len == b->cap) {
        long ncap = b->cap ? b->cap * 2 : 8;
        b->vec = realloc(b->vec, (size_t)ncap * sizeof(long));
        b->cap = ncap;
    }
    b->vec[b->len++] = x;
}

static long fs_pop(FreqStack *s) {
    long top = s->maxfreq;
    BEntry *b = bmap_slot(s->buckets, top);
    long x = b->vec[b->len - 1];
    b->len--;
    int drained = (b->len == 0);
    imap_put(s->freq, x, imap_get(s->freq, x, 0) - 1);
    if (drained) s->maxfreq = top - 1;
    return x;
}

static long run(long rounds, long steps) {
    long checksum = 0;
    FreqStack *st = malloc(sizeof(FreqStack));
    for (long r = 0; r < rounds; r++) {
        fs_init(st);
        long seed = 12345 + r;
        long live = 0;
        for (long i = 0; i < steps; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648L;
            if (i % 3 == 2 && live > 0) {
                checksum += fs_pop(st) * (i % 7 + 1);
                live--;
            } else {
                fs_push(st, seed % 12);
                live++;
            }
        }
        while (live > 0) {
            checksum += fs_pop(st);
            live--;
        }
        fs_free(st);
    }
    free(st);
    return checksum;
}

int main(void) {
    printf("%ld\n", run(120, 3000));
    return 0;
}
