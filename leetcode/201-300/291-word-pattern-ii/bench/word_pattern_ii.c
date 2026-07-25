/* Benchmark harness for LeetCode #291 — Word Pattern II backtracking.
 * Mirrors word_pattern_ii.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map or set, so both are hand-rolled. See the note on
 * the Table struct below for why this is a compact linear scan rather than a
 * hash map, and what that means when reading the numbers.
 */

#include <stdio.h>
#include <string.h>

#define MAXSTR 40
#define CAP 16

typedef char Str[MAXSTR];

/* Small association list with linear scan.
 *
 * An earlier revision of this mirror used open addressing with tombstones, to
 * match the hash maps the other four languages use. That was a mistake: this
 * algorithm inserts and deletes a candidate at EVERY backtracking step, so
 * tombstones accumulated with no compaction and probe chains grew without
 * bound — making C the slowest lane by a wide margin. That was an artifact of
 * the mirror, not a property of C.
 *
 * The map and set never hold more than 3 live entries (the pattern has 3
 * distinct letters), so a linear scan over a compact array is both correct and
 * what a C programmer would actually write here. Deletion swaps in the last
 * element, so there is nothing to accumulate. This IS a fair mirror: it is the
 * natural C data structure for the size, and the README says so plainly rather
 * than implying C and the stdlib-hash-map languages ran identical structures.
 */
typedef struct {
    Str key[CAP];
    Str val[CAP];
    int n;
} Table;

static void str_copy(char *dst, const char *src) {
    size_t n = strlen(src);
    if (n >= MAXSTR) {
        n = MAXSTR - 1;
    }
    memcpy(dst, src, n);
    dst[n] = '\0';
}

static void tbl_clear(Table *t) { t->n = 0; }

static int tbl_find(const Table *t, const char *key) {
    for (int i = 0; i < t->n; i++) {
        if (strcmp(t->key[i], key) == 0) {
            return i;
        }
    }
    return -1;
}

static const char *map_get(const Table *t, const char *key) {
    int i = tbl_find(t, key);
    return i >= 0 ? t->val[i] : 0;
}

static void map_put(Table *t, const char *key, const char *val) {
    int i = tbl_find(t, key);
    if (i < 0) {
        i = t->n++;
        str_copy(t->key[i], key);
    }
    str_copy(t->val[i], val);
}

static void map_del(Table *t, const char *key) {
    int i = tbl_find(t, key);
    if (i >= 0) {
        int last = --t->n;
        if (i != last) {
            str_copy(t->key[i], t->key[last]);
            str_copy(t->val[i], t->val[last]);
        }
    }
}

static int set_has(const Table *t, const char *key) { return tbl_find(t, key) >= 0; }

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
    static Table m;
    static Table used;
    tbl_clear(&m);
    tbl_clear(&used);
    return matches(p, 0, strlen(p), s, 0, strlen(s), &m, &used);
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
