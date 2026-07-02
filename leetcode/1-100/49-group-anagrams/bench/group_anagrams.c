/*
 * LeetCode 49 — sorted-key Group Anagrams, bench mirror in C.
 *
 * Algorithmic mirror of bench/group_anagrams.{kara,rs,py} and go-seq/main.go.
 * Same deterministic input: N=20_000 words of length L=8 drawn from G=1_000
 * classes; each class's letters are L consecutive alphabet letters mod 26, so
 * exactly 26 distinct anagram groups arise. K=40 outer iterations. Stdout
 * sink: K * 26 = 1040.
 *
 * C has no hashmap in libc, so this carries a small open-addressing,
 * linear-probing hashmap keyed by the NUL-terminated sorted string (FNV-1a
 * hash), same shape as kata 1's hash_map.c. The map is reset per call to match
 * Kāra's `Map.new()` per `count_groups` invocation. The 8-char key is sorted
 * with an insertion sort (tiny, branch-cheap for L=8).
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define WORD_LEN 8
#define N 20000
#define G 1000
#define L 8
#define CAP 64 /* power of two, >= 2 * sigma where sigma = 26 here */

static const char ALPHABET[26] = "abcdefghijklmnopqrstuvwxyz";

/* Open-addressing string->i64 map. keys[] hold NUL-terminated sorted words. */
typedef struct {
    char keys[CAP][WORD_LEN + 1];
    int used[CAP];
} Map;

static uint64_t fnv1a(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; ++s) {
        h ^= (uint64_t)(unsigned char)*s;
        h *= 1099511628211ULL;
    }
    return h;
}

/* Insert key if absent; returns 1 when a NEW slot was opened, else 0. */
static int map_touch(Map *m, const char *key) {
    uint64_t idx = fnv1a(key) & (CAP - 1);
    for (;;) {
        if (!m->used[idx]) {
            m->used[idx] = 1;
            memcpy(m->keys[idx], key, WORD_LEN + 1);
            return 1;
        }
        if (strcmp(m->keys[idx], key) == 0) {
            return 0;
        }
        idx = (idx + 1) & (CAP - 1);
    }
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
    memset(m.used, 0, sizeof(m.used));
    long groups = 0;
    char key[WORD_LEN + 1];
    for (int i = 0; i < N; ++i) {
        memcpy(key, words[i], WORD_LEN + 1);
        sort8(key);
        if (map_touch(&m, key)) {
            ++groups;
        }
    }
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
