// LeetCode #1309 bench in C: the ★ arm (the code read from the right, a `#`
// taking the two digits before it, the letters written from the back of a
// fresh `malloc`) on the same 200 codes and 500 passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// the answer, its length in *len; the caller frees it
static char *freq_alphabets(const char *s, size_t n, size_t *len) {
    char *rev = malloc(n + 1);
    size_t count = 0;
    int64_t i = (int64_t)n - 1;
    while (i >= 0) {
        int number;
        if (s[i] == '#') {
            i -= 3;
            number = (s[i + 1] - '0') * 10 + (s[i + 2] - '0');
        } else {
            i -= 1;
            number = s[i + 1] - '0';
        }
        rev[count++] = (char)('a' + number - 1);
    }
    for (size_t a = 0, b = count ? count - 1 : 0; a < b; a++, b--) {
        char t = rev[a];
        rev[a] = rev[b];
        rev[b] = t;
    }
    rev[count] = '\0';
    *len = count;
    return rev;
}

static int64_t seed = 1309;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static size_t encode(const int64_t *letters, int count, char *code) {
    size_t len = 0;
    for (int k = 0; k < count; k++) {
        int64_t v = letters[k] + 1;
        if (v < 10) {
            code[len++] = (char)('0' + v);
        } else {
            code[len++] = (char)('0' + v / 10);
            code[len++] = (char)('0' + v % 10);
            code[len++] = '#';
        }
    }
    code[len] = '\0';
    return len;
}

int main(void) {
    static int64_t texts[200][300];
    static char codes[200][901];
    static size_t lens[200];
    for (int t = 0; t < 200; t++) {
        for (int k = 0; k < 300; k++) texts[t][k] = next_random() % 26;
        lens[t] = encode(texts[t], 300, codes[t]);
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 500; pass++) {
        int64_t t = check % 200;
        texts[t][(check / 200) % 300] = (check / 7) % 26;
        lens[t] = encode(texts[t], 300, codes[t]);
        for (int c = 0; c < 200; c++) {
            size_t len;
            char *got = freq_alphabets(codes[c], lens[c], &len);
            check = (check * 31 + (unsigned char)got[check % (int64_t)len] + (int64_t)len + pass) % 1000000007;
            free(got);
        }
    }
    printf("500 passes over 200 codes: checksum %lld\n", (long long)check);
    return 0;
}
