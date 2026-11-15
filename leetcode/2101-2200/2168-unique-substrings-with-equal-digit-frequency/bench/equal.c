// LeetCode #2168: Unique Substrings With Equal Digit Frequency -- the
// benchmark's C mirror of equal.kara: the set of substrings an
// open-addressing hash table of copies, by FNV-1a.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **keys;
    int64_t *lens;
    uint64_t *hashes;
    int64_t cap, size;
} Set;

static uint64_t fnv(const char *s, int64_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < n; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static void set_init(Set *t, int64_t cap) {
    t->cap = cap;
    t->size = 0;
    t->keys = calloc((size_t)cap, sizeof(char *));
    t->lens = calloc((size_t)cap, sizeof(int64_t));
    t->hashes = calloc((size_t)cap, sizeof(uint64_t));
}

static void set_free(Set *t) {
    for (int64_t i = 0; i < t->cap; i++) free(t->keys[i]);
    free(t->keys);
    free(t->lens);
    free(t->hashes);
}

static void set_put(Set *t, char *key, int64_t len, uint64_t h);

static void grow(Set *t) {
    Set bigger;
    set_init(&bigger, t->cap * 2);
    for (int64_t i = 0; i < t->cap; i++)
        if (t->keys[i]) set_put(&bigger, t->keys[i], t->lens[i], t->hashes[i]);
    free(t->keys);
    free(t->lens);
    free(t->hashes);
    *t = bigger;
}

static void set_put(Set *t, char *key, int64_t len, uint64_t h) {
    int64_t at = (int64_t)(h & (uint64_t)(t->cap - 1));
    while (t->keys[at]) at = (at + 1) & (t->cap - 1);
    t->keys[at] = key;
    t->lens[at] = len;
    t->hashes[at] = h;
    t->size++;
}

static void set_insert(Set *t, const char *s, int64_t len) {
    uint64_t h = fnv(s, len);
    int64_t at = (int64_t)(h & (uint64_t)(t->cap - 1));
    while (t->keys[at]) {
        if (t->hashes[at] == h && t->lens[at] == len && memcmp(t->keys[at], s, (size_t)len) == 0) return;
        at = (at + 1) & (t->cap - 1);
    }
    if ((t->size + 1) * 2 > t->cap) {
        grow(t);
        set_insert(t, s, len);
        return;
    }
    char *copy = malloc((size_t)len);
    memcpy(copy, s, (size_t)len);
    set_put(t, copy, len, h);
}

static int64_t equal_digit_frequency(const char *s, int64_t n) {
    Set found;
    set_init(&found, 64);
    for (int64_t i = 0; i < n; i++) {
        int64_t counts[10] = {0}, kinds = 0, most = 0;
        for (int64_t j = i; j < n; j++) {
            int d = s[j] - '0';
            if (counts[d] == 0) kinds++;
            counts[d]++;
            if (counts[d] > most) most = counts[d];
            if (most * kinds == j - i + 1) set_insert(&found, s + i, j - i + 1);
        }
    }
    int64_t size = found.size;
    set_free(&found);
    return size;
}

static int64_t seed = 2168;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char digits[1000];
    for (int i = 0; i < 1000; i++) digits[i] = (char)('0' + next_random() % 3);
    int64_t check = 0;
    for (int r = 0; r < 200; r++) {
        int64_t at = next_random() % 1000;
        digits[at] = (char)('0' + next_random() % 3);
        check = (check * 31 + equal_digit_frequency(digits, 1000)) % 1000000007;
    }
    printf("200 solves: checksum %lld\n", (long long)check);
    return 0;
}
