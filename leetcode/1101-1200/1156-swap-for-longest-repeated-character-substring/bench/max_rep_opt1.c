// LeetCode #1156 bench -- mirrors max_rep_opt1.kara: the same 64 texts,
// the same passes, the ★ arm's runs.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 20000

static int64_t max_rep_opt1(const unsigned char *b, int64_t n) {
    int64_t count[26] = {0};
    for (int64_t i = 0; i < n; i++) count[b[i] - 'a']++;
    unsigned char *letter = malloc(n);
    int64_t *len = malloc(n * sizeof(int64_t));
    int64_t runs = 0;
    int64_t i = 0;
    while (i < n) {
        int64_t j = i;
        while (j < n && b[j] == b[i]) j++;
        letter[runs] = b[i];
        len[runs] = j - i;
        runs++;
        i = j;
    }
    int64_t best = 0;
    for (int64_t r = 0; r < runs; r++) {
        int64_t have = count[letter[r] - 'a'];
        int64_t grown = len[r] + 1 < have ? len[r] + 1 : have;
        if (grown > best) best = grown;
        if (r + 2 < runs && len[r + 1] == 1 && letter[r + 2] == letter[r]) {
            int64_t joined = len[r] + len[r + 2] + 1;
            if (joined > have) joined = have;
            if (joined > best) best = joined;
        }
    }
    free(letter);
    free(len);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static unsigned char texts[64][N + 64];

int main(void) {
    int64_t passes = 100;
    int64_t seed = 1156;
    const int64_t letters[3] = {2, 3, 26};
    for (int t = 0; t < 64; t++) {
        int64_t n = 0;
        while (n < N) {
            if (t % 4 == 3) {
                int64_t run = 1 + next_random(&seed) % 40;
                for (int64_t q = 0; q < run; q++) texts[t][n++] = 'a';
                texts[t][n++] = 'b' + next_random(&seed) % 25;
            } else {
                texts[t][n++] = 'a' + next_random(&seed) % letters[t % 4];
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++)
        for (int t = 0; t < 64; t++) check = (check * 31 + max_rep_opt1(texts[t], N) + p) % 1000000007;
    printf("%lld passes over 64 texts of 20000 letters: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
