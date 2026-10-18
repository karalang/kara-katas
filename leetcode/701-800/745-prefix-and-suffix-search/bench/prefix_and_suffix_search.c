// LeetCode 745 — Prefix and Suffix Search, bench: the ★ arm (every
// prefix-suffix pair of every word in a hash map) on filters of 10000
// words, each asked 10000 queries. Mirrors prefix_and_suffix_search.kara.
// C has no standard map: this is an open-addressing table of owned
// string keys, hashed by FNV-1a, grown at three quarters full.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char *key; int64_t value; } Slot;
typedef struct { Slot *slots; int64_t cap, len; } Table;

static uint64_t hash(const char *s, size_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (size_t i = 0; i < n; i++) { h ^= (unsigned char)s[i]; h *= 1099511628211ULL; }
    return h;
}

static void grow(Table *t);

static void insert(Table *t, char *key, int64_t value) {  // takes key
    if (4 * (t->len + 1) > 3 * t->cap) grow(t);
    size_t n = strlen(key);
    uint64_t i = hash(key, n) & (t->cap - 1);
    while (t->slots[i].key) {
        if (strcmp(t->slots[i].key, key) == 0) { free(key); t->slots[i].value = value; return; }
        i = (i + 1) & (t->cap - 1);
    }
    t->slots[i].key = key;
    t->slots[i].value = value;
    t->len++;
}

static void grow(Table *t) {
    Table old = *t;
    t->cap = old.cap ? 2 * old.cap : 16;
    t->slots = calloc(t->cap, sizeof(Slot));
    t->len = 0;
    for (int64_t i = 0; i < old.cap; i++)
        if (old.slots[i].key) insert(t, old.slots[i].key, old.slots[i].value);
    free(old.slots);
}

static int64_t lookup(const Table *t, const char *key) {
    uint64_t i = hash(key, strlen(key)) & (t->cap - 1);
    while (t->slots[i].key) {
        if (strcmp(t->slots[i].key, key) == 0) return t->slots[i].value;
        i = (i + 1) & (t->cap - 1);
    }
    return -1;
}

static Table word_filter(char **words, int64_t count) {
    Table t = {0};
    for (int64_t i = 0; i < count; i++) {
        const char *w = words[i];
        int64_t n = strlen(w);
        for (int64_t p = 0; p <= n; p++)
            for (int64_t s = 0; s <= n; s++) {
                char *key = malloc(p + 1 + (n - s) + 1);
                memcpy(key, w, p);
                key[p] = '{';
                memcpy(key + p + 1, w + s, n - s);
                key[p + 1 + n - s] = 0;
                insert(&t, key, i);
            }
    }
    return t;
}

static int64_t f(const Table *t, const char *pref, const char *suff) {
    size_t a = strlen(pref), b = strlen(suff);
    char *key = malloc(a + 1 + b + 1);
    memcpy(key, pref, a);
    key[a] = '{';
    memcpy(key + a + 1, suff, b + 1);
    int64_t got = lookup(t, key);
    free(key);
    return got;
}

static void drop(Table *t) {
    for (int64_t i = 0; i < t->cap; i++) free(t->slots[i].key);
    free(t->slots);
}

static int64_t seed = 745;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *random_word(int64_t longest, int64_t letters) {
    int64_t n = 1 + next_random() % longest;
    char *s = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) s[i] = (char)(97 + next_random() % letters);
    s[n] = 0;
    return s;
}

int main(void) {
    const int64_t rounds = 5, count = 10000, queries = 10000;
    int64_t found = 0, total = 0;
    for (int64_t r = 0; r < rounds; r++) {
        char **words = malloc(count * sizeof(char *));
        for (int64_t i = 0; i < count; i++) words[i] = random_word(7, 5);
        Table t = word_filter(words, count);
        for (int64_t q = 0; q < queries; q++) {
            char *pref = random_word(4, 5);
            char *suff = random_word(4, 5);
            int64_t got = f(&t, pref, suff);
            if (got != -1) { found++; total += got; }
            free(pref);
            free(suff);
        }
        drop(&t);
        for (int64_t i = 0; i < count; i++) free(words[i]);
        free(words);
    }
    printf("%lld rounds of 10000 words and 10000 queries: %lld found, indices sum to %lld\n",
           (long long)rounds, (long long)found, (long long)total);
    return 0;
}
