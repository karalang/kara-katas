// Benchmark: LeetCode #1081 Smallest Subsequence of Distinct Characters --
// the ★ arm. Mirrors smallest_subsequence.kara, .rs, .py and go-seq/. The
// answer is a fresh allocation per call, freed after use, as the String
// the other mirrors return.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *smallest_subsequence(const char *s, int64_t n, int64_t *len) {
    int64_t last[26] = {0};
    for (int64_t i = 0; i < n; i++) last[s[i] - 'a'] = i;
    bool placed[26] = {false};
    char *stack = malloc(27);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        char b = s[i];
        if (placed[b - 'a']) continue;
        while (top > 0) {
            char t = stack[top - 1];
            if (t > b && last[t - 'a'] > i) {
                placed[t - 'a'] = false;
                top--;
            } else {
                break;
            }
        }
        stack[top++] = b;
        placed[b - 'a'] = true;
    }
    stack[top] = 0;
    *len = top;
    return stack;
}

static int64_t seed = 1081;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char texts[2000][1001];

int main(void) {
    int64_t rounds = 100;
    for (int64_t t = 0; t < 2000; t++) {
        int64_t k = t % 26 + 1;
        for (int j = 0; j < 1000; j++) texts[t][j] = (char)('a' + next_random() % k);
        texts[t][1000] = 0;
    }
    int64_t kept = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 2000; i++) {
            int64_t len;
            char *out = smallest_subsequence(texts[(r * 7 + i) % 2000], 1000, &len);
            kept += len;
            check = (check * 31 + (unsigned char)out[len / 2] + i) % 1000000007;
            free(out);
        }
    }
    printf("%lld rounds over 2000 texts of 1000 letters: %lld letters kept, checksum %lld\n", (long long)rounds,
           (long long)kept, (long long)check);
    return 0;
}
