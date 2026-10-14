// Benchmark for #604: C mirror of the ★ arm (read as you go); see
// string_iterator.kara. The text is copied into a `malloc`'d buffer when
// the iterator is made, as the Kāra arm collects it, and freed after.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *text;
    int64_t len, at, left;
    char current;
} StringIterator;

static StringIterator make(const char *compressed) {
    StringIterator it;
    it.len = (int64_t)strlen(compressed);
    it.text = malloc(it.len + 1);
    memcpy(it.text, compressed, it.len + 1);
    it.at = 0;
    it.left = 0;
    it.current = ' ';
    return it;
}

static char next(StringIterator *it) {
    if (it->left == 0) {
        if (it->at == it->len) return ' ';
        it->current = it->text[it->at++];
        int64_t count = 0;
        while (it->at < it->len && it->text[it->at] >= '0' && it->text[it->at] <= '9')
            count = count * 10 + (it->text[it->at++] - 48);
        it->left = count;
    }
    it->left--;
    return it->current;
}

static int has_next(const StringIterator *it) { return it->left > 0 || it->at < it->len; }

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 1000, ROUNDS = 200 };
    int64_t seed = 604;
    static char texts[COUNT][1001];
    for (int t = 0; t < COUNT; t++) {
        size_t len = 0;
        texts[t][0] = 0;
        for (;;) {
            int64_t k = step(&seed) % 52;
            char letter = k < 26 ? (char)(65 + k) : (char)(97 + k - 26);
            int64_t n;
            if (step(&seed) % 10 == 0) {
                int64_t hi = step(&seed);
                int64_t lo = step(&seed);
                n = 1 + (hi * 32768 + lo) % 1000000000;
            } else {
                n = 1 + step(&seed) % 20;
            }
            char run[32];
            int r = snprintf(run, sizeof run, "%c%lld", letter, (long long)n);
            if (len + (size_t)r > 1000) break;
            memcpy(texts[t] + len, run, (size_t)r + 1);
            len += (size_t)r;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            StringIterator it = make(texts[(round * 7 + g) % COUNT]);
            for (int i = 0; i < 50; i++) {
                if (has_next(&it)) total++;
                char c = next(&it);
                checksum = (checksum * 31 + c) % 1000000007;
            }
            free(it.text);
        }
    printf("%d texts, %d rounds: %lld letters left, checksum %lld\n", COUNT, ROUNDS, (long long)total,
           (long long)checksum);
    return 0;
}
