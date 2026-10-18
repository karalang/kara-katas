// LeetCode #730: Count Different Palindromic Subsequences -- by
// interval, with the next and previous copy of the end letter.
// Benchmark mirror of the Kara star arm: the count for each interval
// from the ones inside it, the table kept as rows as the Kara
// program's vector of vectors is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define M 1000000007

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t count_palindromic_subsequences(const char *b, int64_t n) {
    int64_t *next_same = malloc(n * sizeof(int64_t));
    int64_t *prev_same = malloc(n * sizeof(int64_t));
    int64_t last[4] = {-1, -1, -1, -1};
    for (int64_t i = 0; i < n; i++) next_same[i] = n;
    for (int64_t i = 0; i < n; i++) {
        int c = b[i] - 'a';
        prev_same[i] = last[c];
        if (last[c] >= 0) next_same[last[c]] = i;
        last[c] = i;
    }
    int64_t **count = malloc(n * sizeof(int64_t *));
    for (int64_t i = 0; i < n; i++) count[i] = calloc(n, sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        count[i][i] = 1;
        for (int64_t j = i + 1; j < n; j++) {
            int64_t inner = i + 1 <= j - 1 ? count[i + 1][j - 1] : 0;
            int64_t v;
            if (b[i] != b[j]) {
                v = count[i + 1][j] + count[i][j - 1] - inner;
            } else {
                int64_t lo = next_same[i], hi = prev_same[j];
                if (lo > hi)
                    v = 2 * inner + 2;
                else if (lo == hi)
                    v = 2 * inner + 1;
                else
                    v = 2 * inner - (lo + 1 <= hi - 1 ? count[lo + 1][hi - 1] : 0);
            }
            count[i][j] = ((v % M) + M) % M;
        }
    }
    int64_t result = count[0][n - 1];
    for (int64_t i = 0; i < n; i++) free(count[i]);
    free(count);
    free(next_same);
    free(prev_same);
    return result;
}

int main(void) {
    int64_t seed = 730, sum = 0;
    char s[1000];
    for (int r = 0; r < 200; r++) {
        for (int i = 0; i < 1000; i++) s[i] = 'a' + next_random(&seed) % 4;
        sum = (sum + count_palindromic_subsequences(s, 1000)) % M;
    }
    printf("200 strings of 1000 letters: sum %lld\n", (long long)sum);
    return 0;
}
