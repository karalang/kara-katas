// Benchmark for #854: K-Similar Strings -- C twin of the Kāra ★ arm
// (breadth-first search over swaps that fix a letter).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 20

// A set of strings of one length, open addressing on an FNV-1a hash.
typedef struct {
    char *keys;
    unsigned char *used;
    int64_t cap, len, n;
} Seen;

static uint64_t hash(const char *s, int64_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < n; i++) h = (h ^ (unsigned char)s[i]) * 1099511628211ULL;
    return h;
}

static void seen_init(Seen *t, int64_t n) {
    t->cap = 1024;
    t->len = 0;
    t->n = n;
    t->keys = malloc(t->cap * n);
    t->used = calloc(t->cap, 1);
}

static int seen_insert(Seen *t, const char *s);

static void seen_grow(Seen *t) {
    Seen old = *t;
    t->cap *= 2;
    t->len = 0;
    t->keys = malloc(t->cap * t->n);
    t->used = calloc(t->cap, 1);
    for (int64_t i = 0; i < old.cap; i++)
        if (old.used[i]) seen_insert(t, old.keys + i * old.n);
    free(old.keys);
    free(old.used);
}

// Inserts `s`, returning 1 when it was not there before.
static int seen_insert(Seen *t, const char *s) {
    if (2 * (t->len + 1) > t->cap) seen_grow(t);
    uint64_t at = hash(s, t->n) & (t->cap - 1);
    while (t->used[at]) {
        if (memcmp(t->keys + at * t->n, s, t->n) == 0) return 0;
        at = (at + 1) & (t->cap - 1);
    }
    t->used[at] = 1;
    memcpy(t->keys + at * t->n, s, t->n);
    t->len++;
    return 1;
}

static int64_t k_similarity(const char *s1, const char *s2, int64_t n) {
    Seen seen;
    seen_init(&seen, n);
    seen_insert(&seen, s1);
    int64_t cap = 64, len = 1;
    char *level = malloc(cap * n);
    memcpy(level, s1, n);
    int64_t swaps = 0;
    for (;;) {
        int64_t next_cap = 64, next_len = 0;
        char *next = malloc(next_cap * n);
        for (int64_t k = 0; k < len; k++) {
            const char *cur = level + k * n;
            int64_t i = 0;
            while (i < n && cur[i] == s2[i]) i++;
            if (i == n) {
                free(next);
                free(level);
                free(seen.keys);
                free(seen.used);
                return swaps;
            }
            for (int64_t j = i + 1; j < n; j++) {
                if (cur[j] == s2[i] && cur[j] != s2[j]) {
                    char moved[MAXN];
                    memcpy(moved, cur, n);
                    char t = moved[i];
                    moved[i] = moved[j];
                    moved[j] = t;
                    if (seen_insert(&seen, moved)) {
                        if (next_len == next_cap) {
                            next_cap *= 2;
                            next = realloc(next, next_cap * n);
                        }
                        memcpy(next + next_len * n, moved, n);
                        next_len++;
                    }
                }
            }
        }
        free(level);
        level = next;
        len = next_len;
        swaps++;
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 6400, n = MAXN;
    int64_t seed = 854;
    static char firsts[64][MAXN], seconds[64][MAXN];
    for (int64_t g = 0; g < count; g++) {
        int64_t letters = 2 + g % 5;
        for (int64_t i = 0; i < n; i++) firsts[g][i] = 'a' + next_random(&seed) % letters;
        memcpy(seconds[g], firsts[g], n);
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            char t = seconds[g][i];
            seconds[g][i] = seconds[g][j];
            seconds[g][j] = t;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        int64_t k = k_similarity(firsts[g], seconds[g], n);
        total += k;
        checksum = (checksum * 31 + k) % 1000000007;
    }
    printf("%lld rounds of %lld pairs: swaps sum to %lld, checksum %lld\n", (long long)rounds, (long long)count,
           (long long)total, (long long)checksum);
    return 0;
}
