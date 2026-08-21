/* Benchmark twin for LeetCode #294 — same algorithm as flipgame2.kara.
 *
 * PARITY NOTE. Memoized backtracking, one fresh map per board, keyed by the
 * board string with an owned copy stored. C has no string-keyed map in its
 * standard library (`hsearch` is a single process-global table), so idiomatic C
 * for this is a hand-rolled one — an open-addressing table that starts at 16
 * slots and doubles past a 0.7 load factor, which is the same growth discipline
 * the other four languages' maps use. It is faster than a generic map because
 * it is monomorphic and inlined, and that IS C's honest cost here; what would
 * NOT be honest is a fixed table sized from foreknowledge of the workload, or
 * one cleared with a generation counter instead of being rebuilt per board.
 *
 * Successors are built one character at a time rather than by memcpy, matching
 * Kara's append-only String. See #293's bench header for what happened the last
 * time the mirrors drifted into different algorithms.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define LEN 22
#define BOARDS 300

static int64_t next_rand(int64_t s) { return (s * 1103515245 + 12345) & 2147483647; }

/* ---- open-addressing string -> bool map ---------------------------------- */

typedef struct {
    char **keys;      /* NULL slot = empty */
    char *vals;
    size_t cap;       /* power of two */
    size_t count;
} Map;

static uint64_t fnv1a(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    while (*s) {
        h ^= (unsigned char)*s++;
        h *= 1099511628211ULL;
    }
    return h;
}

static void map_init(Map *m) {
    m->cap = 16;
    m->count = 0;
    m->keys = calloc(m->cap, sizeof(char *));
    m->vals = calloc(m->cap, 1);
}

static void map_free(Map *m) {
    for (size_t i = 0; i < m->cap; i++)
        free(m->keys[i]);
    free(m->keys);
    free(m->vals);
}

static void map_put_raw(char **keys, char *vals, size_t cap, char *key, char val) {
    size_t i = (size_t)fnv1a(key) & (cap - 1);
    while (keys[i]) i = (i + 1) & (cap - 1);
    keys[i] = key;
    vals[i] = val;
}

static void map_grow(Map *m) {
    size_t ncap = m->cap * 2;
    char **nkeys = calloc(ncap, sizeof(char *));
    char *nvals = calloc(ncap, 1);
    for (size_t i = 0; i < m->cap; i++)
        if (m->keys[i]) map_put_raw(nkeys, nvals, ncap, m->keys[i], m->vals[i]);
    free(m->keys);
    free(m->vals);
    m->keys = nkeys;
    m->vals = nvals;
    m->cap = ncap;
}

/* Returns 0 or 1 on a hit, -1 on a miss. */
static int map_get(Map *m, const char *key) {
    size_t i = (size_t)fnv1a(key) & (m->cap - 1);
    while (m->keys[i]) {
        if (strcmp(m->keys[i], key) == 0) return m->vals[i];
        i = (i + 1) & (m->cap - 1);
    }
    return -1;
}

static void map_put(Map *m, const char *key, char val) {
    if ((m->count + 1) * 10 > m->cap * 7) map_grow(m);
    map_put_raw(m->keys, m->vals, m->cap, strdup(key), val);
    m->count++;
}

/* ---- the search ---------------------------------------------------------- */

/* Materializes the full successor list before testing any of it, exactly as
 * `next_states` does in the other four mirrors. Building successors lazily
 * inside the loop would be faster -- it skips every successor after the winning
 * one, and needs no allocation at all -- but it is a DIFFERENT algorithm, and
 * the sink cannot tell the difference. That is the #293 mistake; see the note
 * at the top of this file. */
static char **next_states(const char *s, size_t n, int *count) {
    char **out = malloc(sizeof(char *) * (n > 0 ? n : 1));
    int k = 0;
    for (size_t i = 0; i + 1 < n; i++) {
        if (s[i] == '+' && s[i + 1] == '+') {
            char *t = malloc(n + 1);
            for (size_t j = 0; j < n; j++)
                t[j] = (j == i || j == i + 1) ? '-' : s[j];
            t[n] = '\0';
            out[k++] = t;
        }
    }
    *count = k;
    return out;
}

static int can_win(const char *s, Map *memo) {
    int hit = map_get(memo, s);
    if (hit >= 0) return hit;

    size_t n = strlen(s);
    int nstates = 0;
    char **states = next_states(s, n, &nstates);

    int result = 0;
    for (int i = 0; i < nstates; i++) {
        if (!can_win(states[i], memo)) {
            result = 1;
            break;
        }
    }
    for (int i = 0; i < nstates; i++) free(states[i]);
    free(states);

    map_put(memo, s, (char)result);
    return result;
}

int main(void) {
    int64_t seed = 20260821;
    int64_t densities[3] = {15, 50, 85};
    int64_t wins = 0, checksum = 0;
    char s[LEN + 1];

    for (int d = 0; d < 3; d++) {
        for (int b = 0; b < BOARDS; b++) {
            for (int i = 0; i < LEN; i++) {
                seed = next_rand(seed);
                s[i] = ((seed / 65536) % 100) < densities[d] ? '+' : '-';
            }
            s[LEN] = '\0';
            Map memo;
            map_init(&memo);
            if (can_win(s, &memo)) wins++;
            checksum = (checksum * 31 + (int64_t)memo.count) % 1000000007;
            map_free(&memo);
        }
    }
    printf("wins %lld checksum %lld\n", (long long)wins, (long long)checksum);
    return 0;
}
