// Benchmark for #820: Short Encoding of Words -- the ★ arm (a set of the words).
//
// Mirrors short_encoding.kara: put every word in a set, take out every
// proper suffix of every word, and the words left each cost their length
// and a '#'. C has no hash set, so this one is open addressing with an
// FNV-1a hash and a mark for a word taken out; the set holds views into
// the words.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *text;
    int64_t len;
    int removed;
} Slot;

static uint64_t fnv(const char *s, int64_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < n; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }
    return h;
}

// The slot holding the word, or the empty slot where it belongs.
static Slot *find(Slot *table, int64_t cap, const char *s, int64_t n) {
    uint64_t i = fnv(s, n) & (uint64_t)(cap - 1);
    while (table[i].text != NULL) {
        if (table[i].len == n && memcmp(table[i].text, s, (size_t)n) == 0) return &table[i];
        i = (i + 1) & (uint64_t)(cap - 1);
    }
    return &table[i];
}

static int64_t minimum_length_encoding(char **words, int64_t n) {
    int64_t cap = 16;
    while (cap < 2 * n) cap *= 2;
    Slot *kept = calloc((size_t)cap, sizeof(Slot));
    for (int64_t i = 0; i < n; i++) {
        int64_t len = (int64_t)strlen(words[i]);
        Slot *s = find(kept, cap, words[i], len);
        s->text = words[i];
        s->len = len;
    }
    for (int64_t i = 0; i < n; i++) {
        int64_t len = (int64_t)strlen(words[i]);
        for (int64_t k = 1; k < len; k++) {
            Slot *s = find(kept, cap, words[i] + k, len - k);
            if (s->text != NULL) s->removed = 1;
        }
    }
    int64_t total = 0;
    for (int64_t i = 0; i < cap; i++) {
        if (kept[i].text != NULL && !kept[i].removed) total += kept[i].len + 1;
    }
    free(kept);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *random_word(int64_t *seed, int64_t letters, int64_t longest) {
    int64_t length = 1 + next_random(seed) % longest;
    char *word = malloc((size_t)length + 1);
    for (int64_t i = 0; i < length; i++) word[i] = (char)('a' + next_random(seed) % letters);
    word[length] = '\0';
    return word;
}

int main(void) {
    int64_t count = 64;
    int64_t rounds = 12000;
    int64_t seed = 820;
    char **lists[64];
    for (int64_t i = 0; i < count; i++) {
        lists[i] = malloc(2000 * sizeof(char *));
        for (int64_t j = 0; j < 2000; j++) lists[i][j] = random_word(&seed, 5, 7);
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t answer = minimum_length_encoding(lists[round % count], 2000);
        total += answer;
        checksum = (checksum * 131 + answer) % 1000000007;
    }
    printf("%lld rounds of %lld lists of 2000 words: total %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
