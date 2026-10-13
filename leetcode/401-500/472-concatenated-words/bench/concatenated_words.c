// Benchmark for #472 -- C mirror of the ★ arm (concatenated_words.kara):
// shortest first, each word broken against the words before it. The set
// of words is an open-addressing hash table of (pointer, length) keys,
// looked up with a substring in place, as the other languages do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *s;
    size_t n;
} Key;

typedef struct {
    Key *slots;
    size_t mask;
    size_t count;
} Set;

static uint64_t hash(const char *s, size_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (size_t i = 0; i < n; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static void set_init(Set *set, size_t cap) {
    set->slots = calloc(cap, sizeof(Key));
    set->mask = cap - 1;
    set->count = 0;
}

static void set_clear(Set *set) {
    memset(set->slots, 0, (set->mask + 1) * sizeof(Key));
    set->count = 0;
}

static int set_contains(const Set *set, const char *s, size_t n) {
    size_t i = hash(s, n) & set->mask;
    while (set->slots[i].s) {
        if (set->slots[i].n == n && memcmp(set->slots[i].s, s, n) == 0) return 1;
        i = (i + 1) & set->mask;
    }
    return 0;
}

// The key's bytes are not copied: they must outlive the set.
static void set_insert(Set *set, const char *s, size_t n) {
    size_t i = hash(s, n) & set->mask;
    while (set->slots[i].s) {
        if (set->slots[i].n == n && memcmp(set->slots[i].s, s, n) == 0) return;
        i = (i + 1) & set->mask;
    }
    set->slots[i].s = s;
    set->slots[i].n = n;
    set->count++;
}

static int breaks(const char *word, size_t n, const Set *known, char *reach) {
    memset(reach, 0, n + 1);
    reach[0] = 1;
    for (size_t end = 1; end <= n; end++) {
        for (size_t start = 0; start < end; start++) {
            if (reach[start] && set_contains(known, word + start, end - start)) {
                reach[end] = 1;
                break;
            }
        }
    }
    return reach[n];
}

// Writes the indices of the concatenated words to `found` and returns
// how many. `order` is the words sorted by length, stably (by bucket).
static size_t find_all(char **words, size_t *lens, size_t count, Set *known, size_t *order, size_t *found) {
    size_t at = 0;
    for (size_t len = 0; len <= 30; len++)
        for (size_t i = 0; i < count; i++)
            if (lens[i] == len) order[at++] = i;
    set_clear(known);
    char reach[32];
    size_t nfound = 0;
    for (size_t k = 0; k < count; k++) {
        size_t i = order[k];
        if (known->count > 0 && breaks(words[i], lens[i], known, reach)) found[nfound++] = i;
        set_insert(known, words[i], lens[i]);
    }
    return nfound;
}

// ---- bench ------------------------------------------------------------------

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    size_t size = 10000;
    long long seed = 472;
    char **words = malloc(size * sizeof(char *));
    size_t *lens = malloc(size * sizeof(size_t));
    size_t count = 0;
    Set seen;
    set_init(&seen, 32768);
    char buf[128];
    while (count < size) {
        size_t n = 0;
        if (count < 1000) {
            long long letters = 2 + next_random(&seed) % 4;
            for (long long i = 0; i < letters; i++) buf[n++] = (char)(97 + next_random(&seed) % 4);
        } else {
            long long parts = 2 + next_random(&seed) % 2;
            for (long long p = 0; p < parts; p++) {
                size_t i = (size_t)(next_random(&seed) % (long long)count);
                memcpy(buf + n, words[i], lens[i]);
                n += lens[i];
            }
            if (next_random(&seed) % 4 == 0) buf[n++] = 'e';
        }
        if (n <= 30 && !set_contains(&seen, buf, n)) {
            char *w = malloc(n + 1);
            memcpy(w, buf, n);
            w[n] = '\0';
            words[count] = w;
            lens[count] = n;
            set_insert(&seen, w, n);
            count++;
        }
    }
    Set known;
    set_init(&known, 32768);
    size_t *order = malloc(size * sizeof(size_t));
    size_t *found = malloc(size * sizeof(size_t));
    int rounds = 10;
    long long total = 0, hash_sum = 0;
    for (int r = 0; r < rounds; r++) {
        size_t nfound = find_all(words, lens, count, &known, order, found);
        total += (long long)nfound;
        for (size_t k = 0; k < nfound; k++) {
            long long h = 0;
            const char *w = words[found[k]];
            for (size_t j = 0; j < lens[found[k]]; j++) h = (h * 31 + (unsigned char)w[j]) % 1000000007;
            hash_sum = (hash_sum + h) % 1000000007;
        }
    }
    printf("%d rounds on %zu words: %lld concatenated, hash sum %lld\n", rounds, size, total, hash_sum);
    for (size_t i = 0; i < count; i++) free(words[i]);
    free(words);
    free(lens);
    free(order);
    free(found);
    free(seen.slots);
    free(known.slots);
    return 0;
}
