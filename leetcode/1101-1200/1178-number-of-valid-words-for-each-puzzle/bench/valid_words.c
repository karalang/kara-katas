// LeetCode #1178: Number of Valid Words for Each Puzzle -- the ★ arm's
// bench in C: each word's letter set counted in an open-addressing table
// of 32768 slots with linear probing (the words here have at most 9907
// distinct sets), each puzzle's subsets of its other six letters walked with
// `sub = (sub - 1) & rest`. The same words, the same puzzles and the same
// 20 calls.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 32768

typedef struct {
    long *keys;
    long *counts;
    char *used;
} Table;

static long slot(const Table *t, long key) {
    unsigned long i = ((unsigned long)key * 0x9E3779B97F4A7C15UL) >> 49;
    while (t->used[i] && t->keys[i] != key) {
        i = (i + 1) & (SLOTS - 1);
    }
    return (long)i;
}

static void find_num_of_valid_words(char **words, long nw, char **puzzles, long np, long *answer) {
    Table t;
    t.keys = malloc(sizeof(long) * SLOTS);
    t.counts = malloc(sizeof(long) * SLOTS);
    t.used = calloc(SLOTS, 1);
    for (long i = 0; i < nw; i++) {
        long mask = 0;
        for (const char *c = words[i]; *c; c++) {
            mask |= 1L << (*c - 'a');
        }
        long s = slot(&t, mask);
        if (!t.used[s]) {
            t.used[s] = 1;
            t.keys[s] = mask;
            t.counts[s] = 0;
        }
        t.counts[s] += 1;
    }
    for (long i = 0; i < np; i++) {
        const char *p = puzzles[i];
        long first = 1L << (p[0] - 'a');
        long rest = 0;
        for (const char *c = p + 1; *c; c++) {
            rest |= 1L << (*c - 'a');
        }
        long total = 0;
        long sub = rest;
        for (;;) {
            long s = slot(&t, sub | first);
            if (t.used[s]) {
                total += t.counts[s];
            }
            if (sub == 0) {
                break;
            }
            sub = (sub - 1) & rest;
        }
        answer[i] = total;
    }
    free(t.keys);
    free(t.counts);
    free(t.used);
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static void distinct(long *seed, long m, long k, char *out) {
    char letters[26];
    for (long i = 0; i < m; i++) {
        letters[i] = (char)('a' + i);
    }
    for (long i = 0; i < k; i++) {
        long j = i + next_random(seed) % (m - i);
        char x = letters[i];
        letters[i] = letters[j];
        letters[j] = x;
    }
    memcpy(out, letters, k);
}

int main(void) {
    long seed = 1178;
    long nw = 100000, np = 10000;
    char **words = malloc(sizeof(char *) * nw);
    for (long i = 0; i < nw; i++) {
        char set[7];
        long k = 1 + next_random(&seed) % 7;
        distinct(&seed, 14, k, set);
        long len = 4 + next_random(&seed) % 47;
        words[i] = malloc(len + 1);
        for (long j = 0; j < len; j++) {
            words[i][j] = set[next_random(&seed) % k];
        }
        words[i][len] = 0;
    }
    char **puzzles = malloc(sizeof(char *) * np);
    for (long i = 0; i < np; i++) {
        puzzles[i] = malloc(8);
        distinct(&seed, 14, 7, puzzles[i]);
        puzzles[i][7] = 0;
    }
    long *answer = malloc(sizeof(long) * np);
    long calls = 20;
    long check = 0;
    for (long c = 0; c < calls; c++) {
        find_num_of_valid_words(words, nw, puzzles, np, answer);
        for (long i = 0; i < np; i++) {
            check = (check * 131 + answer[i] + 1) % 1000000007;
        }
    }
    printf("%ld calls: checksum %ld\n", calls, check);
    return 0;
}
