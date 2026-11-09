// LeetCode #2047 -- the ★ arm as a benchmark; mirror of valid.kara: the
// sentence walked token by token, each token checked by index.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int is_lower(char c) { return c >= 'a' && c <= 'z'; }

static int is_valid(const char *t, int64_t n) {
    int64_t hyphens = 0;
    for (int64_t i = 0; i < n; i++) {
        char c = t[i];
        if (c >= '0' && c <= '9') return 0;
        if (c == '-') {
            hyphens++;
            if (hyphens > 1 || i == 0 || i == n - 1) return 0;
            if (!is_lower(t[i - 1]) || !is_lower(t[i + 1])) return 0;
        }
        if ((c == '!' || c == '.' || c == ',') && i != n - 1) return 0;
    }
    return 1;
}

static int64_t count_valid_words(const char *s, int64_t len) {
    int64_t count = 0, i = 0;
    while (i < len) {
        while (i < len && s[i] == ' ') i++;
        int64_t start = i;
        while (i < len && s[i] != ' ') i++;
        if (i > start && is_valid(s + start, i - start)) count++;
    }
    return count;
}

static int64_t seed = 2047;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char *symbols = "abcdefgh--!.,9";
    int64_t nsym = 14;
    char *sentences = malloc(2000 * 1000);
    for (int64_t k = 0; k < 2000; k++) {
        for (int64_t j = 0; j < 1000; j++) {
            int64_t r = next_random() % 100;
            char c;
            if (r < 70) c = symbols[next_random() % 8];
            else if (r < 85) c = ' ';
            else c = symbols[next_random() % nsym];
            sentences[k * 1000 + j] = c;
        }
    }
    int64_t calls = 0, words = 0, check = 0;
    for (int64_t r = 0; r < 100; r++) {
        for (int64_t k = 0; k < 2000; k++) {
            int64_t off = r % 7;
            int64_t n = count_valid_words(sentences + k * 1000 + off, 1000 - off);
            calls++;
            words += n;
            check = (check * 31 + n) % 1000000007;
        }
    }
    printf("%lld calls: %lld valid words, checksum %lld\n", (long long)calls,
           (long long)words, (long long)check);
    free(sentences);
    return 0;
}
