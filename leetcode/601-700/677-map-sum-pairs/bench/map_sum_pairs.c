// Benchmark for #677: the keys kept sorted, as the Kara sorted arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 677;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

typedef struct {
    char **keys;
    int64_t *vals;
    int64_t len, cap;
} MapSum;

static int64_t lower_bound(char **keys, int64_t n, const char *word) {
    int64_t lo = 0, hi = n;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (strcmp(keys[mid], word) < 0) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static void insert(MapSum *m, char *key, int64_t val) {
    int64_t at = lower_bound(m->keys, m->len, key);
    if (at < m->len && strcmp(m->keys[at], key) == 0) {
        m->vals[at] = val;
        free(key);
        return;
    }
    if (m->len == m->cap) {
        m->cap = m->cap ? m->cap * 2 : 4;
        m->keys = realloc(m->keys, sizeof(char *) * m->cap);
        m->vals = realloc(m->vals, sizeof(int64_t) * m->cap);
    }
    memmove(m->keys + at + 1, m->keys + at, sizeof(char *) * (m->len - at));
    memmove(m->vals + at + 1, m->vals + at, sizeof(int64_t) * (m->len - at));
    m->keys[at] = key;
    m->vals[at] = val;
    m->len++;
}

static int64_t sum(const MapSum *m, const char *prefix) {
    size_t n = strlen(prefix);
    int64_t total = 0;
    for (int64_t i = lower_bound(m->keys, m->len, prefix);
         i < m->len && strncmp(m->keys[i], prefix, n) == 0; i++) {
        total += m->vals[i];
    }
    return total;
}

static char *random_word(int64_t most) {
    int64_t n = 1 + next_random() % most;
    char *s = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) s[i] = (char)(97 + next_random() % 3);
    s[n] = 0;
    return s;
}

int main(void) {
    int64_t rounds = 100;
    int64_t calls = 2000;
    int64_t s = 0;
    for (int64_t r = 0; r < rounds; r++) {
        MapSum m = {0};
        for (int64_t k = 0; k < calls; k++) {
            char *key = random_word(12);
            insert(&m, key, 1 + next_random() % 1000);
        }
        for (int64_t k = 0; k < calls; k++) {
            char *prefix = random_word(3);
            s = (s * 31 + sum(&m, prefix)) % 1000000007;
            free(prefix);
        }
        for (int64_t i = 0; i < m.len; i++) free(m.keys[i]);
        free(m.keys);
        free(m.vals);
    }
    printf("%lld rounds of %lld inserts and %lld sums: checksum %lld\n", (long long)rounds,
           (long long)calls, (long long)calls, (long long)s);
    return 0;
}
