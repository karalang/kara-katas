/*
 * LeetCode 49 — sorted-key Group Anagrams, bench mirror in C.
 *
 * Algorithmic mirror of bench/group_anagrams.{kara,rs,py} and go-seq/main.go.
 * Same deterministic input: N=20_000 words of length L=8 drawn from G=1_000
 * classes; each class's letters are L consecutive alphabet letters mod 26, so
 * exactly 26 distinct anagram groups arise. K=40 outer iterations. Stdout
 * sink: K * 26 = 1040.
 *
 * C has no hashmap in libc, so this carries an open-addressing, linear-probing
 * hashmap keyed by the NUL-terminated sorted string. The 8-char key is sorted
 * with an insertion sort (tiny, branch-cheap for L=8).
 *
 * The table is shaped to match the runtime's Map[K,V] rather than presized to
 * the workload:
 *
 *   - heap-allocated per call, like the kata's `Map.new()`, and freed on the
 *     way out;
 *   - capacity 16 initially, power of two, linear probing;
 *   - grow (double + full rehash) when (len + 1) * 4 > capacity * 3, i.e. the
 *     same 75% load factor as the runtime map;
 *   - FxHash over the key bytes with the same seed and rotate the compiler
 *     synthesizes (h = rotl(h,5) ^ byte; h *= SEED, from h = 0), replacing the
 *     FNV-1a this mirror used.
 *
 * The previous fixed 64-entry stack table was presized to just past the
 * 26-key working set, so it never allocated, grew, or rehashed, while the
 * kata's map climbs 16 -> 32 -> 64 on each of the 40 calls. Presizing to the
 * answer is not a C advantage, it is a different program.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WORD_LEN 8
#define N 20000
#define G 1000
#define L 8

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

static const char ALPHABET[26] = "abcdefghijklmnopqrstuvwxyz";

/* Open-addressing string->i64 map. keys[] hold NUL-terminated sorted words. */
typedef struct {
    char (*keys)[WORD_LEN + 1];
    long long *vals;
    unsigned char *used;
    size_t cap;
    size_t len;
} Map;

static uint64_t fxhash(const char *s) {
    uint64_t h = 0;
    for (; *s; ++s) {
        h = ((h << 5) | (h >> 59)) ^ (uint64_t)(unsigned char)*s;
        h *= FXHASH_SEED;
    }
    return h;
}

static void map_init(Map *m) {
    m->cap = INITIAL_CAPACITY;
    m->len = 0;
    m->keys = malloc(m->cap * (WORD_LEN + 1));
    m->vals = malloc(m->cap * sizeof(long long));
    m->used = calloc(m->cap, 1);
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->vals);
    free(m->used);
}

static size_t map_slot(const Map *m, const char *key) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash(key) & mask;
    while (m->used[h] && strcmp(m->keys[h], key) != 0) {
        h = (h + 1) & mask;
    }
    return h;
}

static void map_grow(Map *m) {
    char(*ok)[WORD_LEN + 1] = m->keys;
    long long *ov = m->vals;
    unsigned char *ou = m->used;
    size_t ocap = m->cap;

    m->cap = ocap * 2;
    m->keys = malloc(m->cap * (WORD_LEN + 1));
    m->vals = malloc(m->cap * sizeof(long long));
    m->used = calloc(m->cap, 1);

    for (size_t i = 0; i < ocap; i++) {
        if (ou[i]) {
            size_t h = map_slot(m, ok[i]);
            m->used[h] = 1;
            memcpy(m->keys[h], ok[i], WORD_LEN + 1);
            m->vals[h] = ov[i];
        }
    }
    free(ok);
    free(ov);
    free(ou);
}

/* Insert key if absent; returns 1 when a NEW slot was opened, else 0. */
static int map_touch(Map *m, const char *key, long long v) {
    size_t h = map_slot(m, key);
    if (m->used[h]) {
        return 0;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((m->len + 1) * 4 > m->cap * 3) {
        map_grow(m);
        h = map_slot(m, key);
    }
    m->used[h] = 1;
    memcpy(m->keys[h], key, WORD_LEN + 1);
    m->vals[h] = v;
    m->len++;
    return 1;
}

static void sort8(char *w) {
    for (int i = 1; i < WORD_LEN; ++i) {
        char c = w[i];
        int j = i - 1;
        while (j >= 0 && w[j] > c) {
            w[j + 1] = w[j];
            --j;
        }
        w[j + 1] = c;
    }
}

static long count_groups(char words[N][WORD_LEN + 1]) {
    Map m;
    map_init(&m);
    long groups = 0;
    char key[WORD_LEN + 1];
    for (int i = 0; i < N; ++i) {
        memcpy(key, words[i], WORD_LEN + 1);
        sort8(key);
        if (map_touch(&m, key, groups)) {
            ++groups;
        }
    }
    map_free(&m);
    return groups;
}

int main(void) {
    static char words[N][WORD_LEN + 1];
    for (int i = 0; i < N; ++i) {
        int grp = i % G;
        int rot = (i / G) % L;
        char seed[WORD_LEN];
        for (int k = 0; k < L; ++k) {
            seed[k] = ALPHABET[(grp + k) % 26];
        }
        int p = 0;
        for (int k = rot; k < L; ++k) {
            words[i][p++] = seed[k];
        }
        for (int k = 0; k < rot; ++k) {
            words[i][p++] = seed[k];
        }
        words[i][WORD_LEN] = '\0';
    }

    long total = 0;
    for (int it = 0; it < 40; ++it) {
        total += count_groups(words);
    }
    printf("%ld\n", total);
    return 0;
}
