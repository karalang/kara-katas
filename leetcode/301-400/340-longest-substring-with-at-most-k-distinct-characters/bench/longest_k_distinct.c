// Benchmark mirror of longest_k_distinct.kara (LeetCode #340): a sliding
// window with a count per character in a hash map. C has no standard map,
// so this is a small open-addressing table (linear probing, backward-shift
// deletion) keyed by the character. Same strings, rounds and sink.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 128

typedef struct {
    int32_t key[SLOTS];  // -1 = empty
    int64_t val[SLOTS];
    int64_t len;
} Counts;

static uint32_t slot_of(int32_t c) { return ((uint32_t)c * 2654435761u) >> 25; }

static void counts_clear(Counts *m) {
    memset(m->key, 0xff, sizeof m->key);
    m->len = 0;
}

static int64_t *counts_find(Counts *m, int32_t c) {
    for (uint32_t i = slot_of(c);; i = (i + 1) & (SLOTS - 1)) {
        if (m->key[i] == c) return &m->val[i];
        if (m->key[i] < 0) return NULL;
    }
}

static void counts_add(Counts *m, int32_t c) {
    uint32_t i = slot_of(c);
    while (m->key[i] >= 0 && m->key[i] != c) i = (i + 1) & (SLOTS - 1);
    if (m->key[i] < 0) {
        m->key[i] = c;
        m->val[i] = 0;
        m->len++;
    }
    m->val[i]++;
}

static void counts_remove(Counts *m, int32_t c) {
    uint32_t i = slot_of(c);
    while (m->key[i] != c) i = (i + 1) & (SLOTS - 1);
    m->key[i] = -1;
    m->len--;
    // Backward shift: pull later members of the probe run into the hole.
    for (uint32_t j = (i + 1) & (SLOTS - 1); m->key[j] >= 0; j = (j + 1) & (SLOTS - 1)) {
        uint32_t home = slot_of(m->key[j]);
        if (((j - home) & (SLOTS - 1)) >= ((j - i) & (SLOTS - 1))) {
            m->key[i] = m->key[j];
            m->val[i] = m->val[j];
            m->key[j] = -1;
            i = j;
        }
    }
}

static int64_t longest_k_distinct(const char *s, int64_t n, int64_t k) {
    Counts m;
    counts_clear(&m);
    int64_t left = 0, best = 0;
    for (int64_t right = 0; right < n; right++) {
        counts_add(&m, s[right]);
        while (m.len > k) {
            int32_t d = s[left];
            int64_t *v = counts_find(&m, d);
            if (--*v == 0) counts_remove(&m, d);
            left++;
        }
        if (right - left + 1 > best) best = right - left + 1;
    }
    return best;
}

static int64_t next(int64_t *state) {
    *state = (*state * 1103515245 + 12345) % 2147483648;
    return *state >> 8;
}

static char *gen_text(int64_t seed, int64_t n, int64_t alpha) {
    const char *letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int64_t state = seed;
    char *out = malloc((size_t)n + 1);
    for (int64_t i = 0; i < n; i++) out[i] = letters[next(&state) % alpha];
    out[n] = 0;
    return out;
}

int main(void) {
    const int64_t alphas[8] = {4, 8, 12, 20, 26, 34, 44, 52};
    char *texts[8];
    for (int i = 0; i < 8; i++) texts[i] = gen_text(1000 + i, 20000, alphas[i]);
    int64_t h = 0;
    for (int64_t r = 0; r < 400; r++) {
        int64_t k = (r * 7) % 30 + 1;
        h = (h * 31 + longest_k_distinct(texts[r % 8], 20000, k)) % 1000000007;
    }
    printf("%lld\n", (long long)h);
    for (int i = 0; i < 8; i++) free(texts[i]);
    return 0;
}
