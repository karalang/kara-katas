// LeetCode #2707: Extra Characters in a String -- the bench (extra.kara in
// C): the fewest extra characters of each suffix, from the end back, with
// the dictionary a hash set (open addressing, FNV-1a) asked about every
// slice.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 128

typedef struct {
    const char *text[SLOTS];
    int len[SLOTS];
} WordSet;

static uint64_t fnv(const char *p, int n) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < n; i++) {
        h ^= (unsigned char)p[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static void insert(WordSet *set, const char *p, int n) {
    uint64_t h = fnv(p, n) & (SLOTS - 1);
    while (set->text[h]) {
        if (set->len[h] == n && memcmp(set->text[h], p, n) == 0) return;
        h = (h + 1) & (SLOTS - 1);
    }
    set->text[h] = p;
    set->len[h] = n;
}

static int contains(const WordSet *set, const char *p, int n) {
    uint64_t h = fnv(p, n) & (SLOTS - 1);
    while (set->text[h]) {
        if (set->len[h] == n && memcmp(set->text[h], p, n) == 0) return 1;
        h = (h + 1) & (SLOTS - 1);
    }
    return 0;
}

static int64_t min_extra_char(const char *s, int n, char words[][6], const int *lens, int count) {
    WordSet set;
    memset(&set, 0, sizeof set);
    for (int w = 0; w < count; w++) insert(&set, words[w], lens[w]);
    int64_t best[51];
    best[n] = 0;
    for (int i = n - 1; i >= 0; i--) {
        best[i] = best[i + 1] + 1;
        for (int j = i + 1; j <= n; j++) {
            if (contains(&set, s + i, j - i) && best[j] < best[i]) best[i] = best[j];
        }
    }
    return best[0];
}

static int64_t seed = 2707;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    char s[51];
    char words[50][6];
    int lens[50];
    int count;
} Problem;

int main(void) {
    const int cases = 10000, rounds = 5;
    Problem *problems = calloc(cases, sizeof(Problem));
    for (int c = 0; c < cases; c++) {
        Problem *p = &problems[c];
        for (int i = 0; i < 50; i++) p->s[i] = (char)('a' + next_random() % 3);
        for (int w = 0; w < 50; w++) {
            int n = (int)(next_random() % 5 + 1);
            char word[6] = {0};
            for (int i = 0; i < n; i++) word[i] = (char)('a' + next_random() % 3);
            int seen = 0;
            for (int k = 0; k < p->count; k++) {
                if (p->lens[k] == n && memcmp(p->words[k], word, n) == 0) seen = 1;
            }
            if (!seen) {
                memcpy(p->words[p->count], word, 6);
                p->lens[p->count] = n;
                p->count++;
            }
        }
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < cases; c++) {
            Problem *p = &problems[c];
            int64_t extra = min_extra_char(p->s, 50, p->words, p->lens, p->count);
            sum += extra;
            check = (check * 31 + extra + r) % 1000000007;
        }
    }
    printf("%d strings of 50 letters against up to 50 words, %d rounds: extra characters sum to %lld, checksum %lld\n", cases, rounds, (long long)sum, (long long)check);
    free(problems);
    return 0;
}
