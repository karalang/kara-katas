// LeetCode #734: Sentence Similarity -- a set of pairs.
// Benchmark mirror of the Kara star arm: put every pair in a hash set
// both ways round, then check the words place by place. The set holds
// pointers to the words rather than copies, as C would, and so do Go's
// strings and Python's tuples; the Kara and Rust programs clone the
// words into the set.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *a, *b;
} Pair;

static uint64_t hash_pair(const char *a, const char *b) {
    uint64_t h = 1469598103934665603ULL;
    for (const char *p = a; *p; p++) h = (h ^ (unsigned char)*p) * 1099511628211ULL;
    h = (h ^ 0xff) * 1099511628211ULL;
    for (const char *p = b; *p; p++) h = (h ^ (unsigned char)*p) * 1099511628211ULL;
    return h;
}

typedef struct {
    Pair *slots;
    uint64_t cap, len;
} Set;

static int set_contains(Set *s, const char *a, const char *b) {
    uint64_t i = hash_pair(a, b) & (s->cap - 1);
    while (s->slots[i].a) {
        if (strcmp(s->slots[i].a, a) == 0 && strcmp(s->slots[i].b, b) == 0) return 1;
        i = (i + 1) & (s->cap - 1);
    }
    return 0;
}

static void set_insert(Set *s, const char *a, const char *b) {
    if ((s->len + 1) * 2 > s->cap) {
        Set bigger = {calloc(s->cap * 2, sizeof(Pair)), s->cap * 2, 0};
        for (uint64_t i = 0; i < s->cap; i++)
            if (s->slots[i].a) set_insert(&bigger, s->slots[i].a, s->slots[i].b);
        free(s->slots);
        *s = bigger;
    }
    uint64_t i = hash_pair(a, b) & (s->cap - 1);
    while (s->slots[i].a) {
        if (strcmp(s->slots[i].a, a) == 0 && strcmp(s->slots[i].b, b) == 0) return;
        i = (i + 1) & (s->cap - 1);
    }
    s->slots[i] = (Pair){a, b};
    s->len++;
}

static int are_sentences_similar(char **s1, char **s2, int64_t n, Pair *pairs, int64_t np) {
    Set similar = {calloc(16, sizeof(Pair)), 16, 0};
    for (int64_t i = 0; i < np; i++) {
        set_insert(&similar, pairs[i].a, pairs[i].b);
        set_insert(&similar, pairs[i].b, pairs[i].a);
    }
    int ok = 1;
    for (int64_t i = 0; i < n && ok; i++)
        if (strcmp(s1[i], s2[i]) != 0 && !set_contains(&similar, s1[i], s2[i])) ok = 0;
    free(similar.slots);
    return ok;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *word(int64_t k) {
    char *w = malloc(16);
    snprintf(w, 16, "w%lld", (long long)k);
    return w;
}

int main(void) {
    int64_t seed = 734;
    Pair pairs[1000];
    for (int i = 0; i < 1000; i++) {
        int64_t a = next_random(&seed) % 5000;
        int64_t b = next_random(&seed) % 5000;
        pairs[i] = (Pair){word(a), word(b)};
    }
    char *s1[1000], *s2[1000];
    for (int i = 0; i < 1000; i++) {
        int64_t p = next_random(&seed) % 1000;
        if (next_random(&seed) % 2 == 0) {
            s1[i] = strdup(pairs[p].a);
            s2[i] = strdup(pairs[p].b);
        } else {
            s1[i] = strdup(pairs[p].b);
            s2[i] = strdup(pairs[p].a);
        }
    }
    int64_t similar = 0;
    for (int round = 0; round < 1000; round++) {
        int64_t j = next_random(&seed) % 1000;
        int64_t x = next_random(&seed) % 5000;
        char *saved = s2[j];
        s2[j] = word(x);
        similar += are_sentences_similar(s1, s2, 1000, pairs, 1000);
        free(s2[j]);
        s2[j] = saved;
        similar += are_sentences_similar(s1, s2, 1000, pairs, 1000);
    }
    printf("1000 rounds of 2 checks of 1000 words with 1000 pairs: %lld similar\n", (long long)similar);
    return 0;
}
