// Benchmark for #425: mirror of word_squares.kara (a map of prefixes).
// The map is a table indexed by the prefix read as a number in base 27,
// with a growable list of word indexes per prefix. Each square found is
// copied out as its own strings, as the Kāra program clones its rows.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t *items; int64_t len, cap; } List;
typedef struct { char **rows; } Square;

static List *by_prefix;
static char **words;
static int64_t length;
static Square *found;
static int64_t found_len, found_cap;
static int64_t rows[8];

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof *l->items);
    }
    l->items[l->len++] = v;
}

static void extend(int64_t r) {
    if (r == length) {
        if (found_len == found_cap) {
            found_cap = found_cap ? found_cap * 2 : 1024;
            found = realloc(found, found_cap * sizeof *found);
        }
        Square s;
        s.rows = malloc(length * sizeof *s.rows);
        for (int64_t i = 0; i < length; i++) {
            s.rows[i] = malloc(length + 1);
            memcpy(s.rows[i], words[rows[i]], length + 1);
        }
        found[found_len++] = s;
        return;
    }
    int64_t key = 0;
    for (int64_t i = 0; i < r; i++) key = key * 27 + (words[rows[i]][r] - 'a' + 1);
    List *candidates = &by_prefix[key];
    for (int64_t c = 0; c < candidates->len; c++) {
        rows[r] = candidates->items[c];
        extend(r + 1);
    }
}

static void word_squares(int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        int64_t key = 0;
        for (int64_t k = 0; k < length; k++) {
            push(&by_prefix[key], i);
            key = key * 27 + (words[i][k] - 'a' + 1);
        }
    }
    found_len = 0;
    extend(0);
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static void random_word(int64_t *seed, char *out) {
    for (int k = 0; k < 4; k++) out[k] = (char)('a' + step(seed) % 16);
    out[4] = 0;
}

static int code(const char *w) {
    return ((w[0] - 'a') * 16 + (w[1] - 'a')) * 256 + (w[2] - 'a') * 16 + (w[3] - 'a');
}

int main(int argc, char **argv) {
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 20;
    int64_t n = 1000, seed = 425;
    length = 4;
    char *seen = calloc(65536, 1);
    words = malloc(n * sizeof *words);
    int64_t count = 0;
    while (count < n) {
        char w[5];
        random_word(&seed, w);
        if (!seen[code(w)]) {
            seen[code(w)] = 1;
            words[count] = malloc(5);
            memcpy(words[count], w, 5);
            count++;
        }
    }
    int64_t keys = 27 * 27 * 27 * 27;
    by_prefix = calloc(keys, sizeof *by_prefix);
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        char w[5];
        random_word(&seed, w);
        while (seen[code(w)]) random_word(&seed, w);
        int64_t at = r * 389 % n;
        seen[code(words[at])] = 0;
        seen[code(w)] = 1;
        memcpy(words[at], w, 5);
        for (int64_t k = 0; k < keys; k++) by_prefix[k].len = 0;
        word_squares(n);
        total += found_len;
        for (int64_t s = 0; s < found_len; s++) {
            checksum = (checksum * 31 + found[s].rows[0][0] + found[s].rows[3][3]) % 1000000007;
            for (int64_t i = 0; i < length; i++) free(found[s].rows[i]);
            free(found[s].rows);
        }
    }
    printf("%lld rounds on %lld words: %lld squares, checksum %lld\n", (long long)rounds, (long long)n, (long long)total, (long long)checksum);
    return 0;
}
