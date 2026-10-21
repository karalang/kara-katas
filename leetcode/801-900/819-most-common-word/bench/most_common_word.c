// Benchmark for #819: Most Common Word -- the ★ arm (a map of counts).
//
// Mirrors most_common_word.kara: lower every letter and turn everything
// else into a space, count each word that is not banned in a hash table,
// and return the word counted most, the first alphabetically of two
// counted as often. C has no hash table, so this one is open addressing
// with an FNV-1a hash; the words are views into the cleaned text.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *text;
    int64_t len;
    int64_t count;
} Slot;

static uint64_t fnv(const char *s, int64_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < n; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static int64_t pow2_at_least(int64_t n) {
    int64_t c = 16;
    while (c < n) c *= 2;
    return c;
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

static int less(const char *a, int64_t an, const char *b, int64_t bn) {
    int64_t n = an < bn ? an : bn;
    int c = memcmp(a, b, (size_t)n);
    return c < 0 || (c == 0 && an < bn);
}

// Writes the answer into `out` and returns its length.
static int64_t most_common_word(const char *paragraph, int64_t len, char **banned, int64_t nbanned,
                                char *out) {
    char *cleaned = malloc((size_t)len + 1);
    for (int64_t i = 0; i < len; i++) {
        char c = paragraph[i];
        if (c >= 'A' && c <= 'Z') cleaned[i] = (char)(c + 32);
        else if (c >= 'a' && c <= 'z') cleaned[i] = c;
        else cleaned[i] = ' ';
    }
    int64_t bcap = pow2_at_least(2 * nbanned);
    Slot *ruled_out = calloc((size_t)bcap, sizeof(Slot));
    for (int64_t k = 0; k < nbanned; k++) {
        int64_t n = (int64_t)strlen(banned[k]);
        Slot *s = find(ruled_out, bcap, banned[k], n);
        s->text = banned[k];
        s->len = n;
    }
    int64_t cap = pow2_at_least(len + 2);
    Slot *counts = calloc((size_t)cap, sizeof(Slot));
    int64_t i = 0;
    while (i < len) {
        if (cleaned[i] == ' ') {
            i++;
            continue;
        }
        int64_t start = i;
        while (i < len && cleaned[i] != ' ') i++;
        if (find(ruled_out, bcap, cleaned + start, i - start)->text != NULL) continue;
        Slot *s = find(counts, cap, cleaned + start, i - start);
        if (s->text == NULL) {
            s->text = cleaned + start;
            s->len = i - start;
        }
        s->count++;
    }
    const char *best = "";
    int64_t best_len = 0, most = 0;
    for (int64_t k = 0; k < cap; k++) {
        Slot *s = &counts[k];
        if (s->text == NULL) continue;
        if (s->count > most || (s->count == most && less(s->text, s->len, best, best_len))) {
            best = s->text;
            best_len = s->len;
            most = s->count;
        }
    }
    memcpy(out, best, (size_t)best_len);
    free(counts);
    free(ruled_out);
    free(cleaned);
    return best_len;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *random_word(int64_t *seed) {
    int64_t length = 1 + next_random(seed) % 10;
    char *w = malloc((size_t)length + 1);
    for (int64_t i = 0; i < length; i++) w[i] = (char)('a' + next_random(seed) % 26);
    w[length] = 0;
    return w;
}

int main(void) {
    enum { COUNT = 64 };
    int64_t rounds = 200000;
    int64_t seed = 819;
    const char *marks[] = {" ", " ", " ", ", ", ". ", "! ", "? ", "; ", "' ", ","};
    char *vocabulary[300];
    for (int k = 0; k < 300; k++) vocabulary[k] = random_word(&seed);
    char *paragraphs[COUNT];
    int64_t lengths[COUNT];
    char *banned[COUNT][100];
    for (int g = 0; g < COUNT; g++) {
        char *p = malloc(1100);
        int64_t n = 0;
        while (n < 990) {
            int64_t a = next_random(&seed) % 300;
            int64_t k = a * (next_random(&seed) % 300) / 300;
            int upper = next_random(&seed) % 4 == 0;
            for (const char *c = vocabulary[k]; *c; c++) p[n++] = upper ? (char)(*c - 32) : *c;
            const char *m = marks[next_random(&seed) % 10];
            for (; *m; m++) p[n++] = *m;
        }
        p[n] = 0;
        paragraphs[g] = p;
        lengths[g] = n;
        for (int k = 0; k < 50; k++) banned[g][k] = vocabulary[next_random(&seed) % 30];
        for (int k = 50; k < 100; k++) banned[g][k] = random_word(&seed);
    }
    int64_t total = 0, checksum = 0;
    char answer[64];
    for (int64_t round = 0; round < rounds; round++) {
        int g = (int)(round % COUNT);
        int64_t n = most_common_word(paragraphs[g], lengths[g], banned[g], 100, answer);
        total += n;
        for (int64_t i = 0; i < n; i++) checksum = (checksum * 131 + (unsigned char)answer[i]) % 1000000007;
    }
    printf("%lld rounds of %d paragraphs: total %lld, checksum %lld\n", (long long)rounds, COUNT,
           (long long)total, (long long)checksum);
    return 0;
}
