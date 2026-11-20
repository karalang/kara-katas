// LeetCode #1668: Maximum Repeating Substring -- the bench's C mirror: the
// ★ arm on 400000 problems, words of 1 to 6 letters and sequences of about
// 100 built of whole copies of the word and single letters, all drawn
// first. The search is libc's `strstr`.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PROBLEMS 400000

static int32_t max_repeating(const char *sequence, const char *word) {
    int32_t k = 0;
    size_t m = strlen(word), n = strlen(sequence);
    char *repeated = malloc(n + m + 1);
    memcpy(repeated, word, m + 1);
    size_t len = m;
    while (strstr(sequence, repeated)) {
        k++;
        memcpy(repeated + len, word, m + 1);
        len += m;
    }
    free(repeated);
    return k;
}

// ---- the harness --------------------------------------------------------

static int64_t seed = 1668;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char words[PROBLEMS][8];
    static char sequences[PROBLEMS][112];
    for (int p = 0; p < PROBLEMS; p++) {
        int64_t kinds = next_random() % 3 + 1;
        int64_t m = next_random() % 6 + 1;
        for (int64_t i = 0; i < m; i++) words[p][i] = (char)('a' + next_random() % kinds);
        words[p][m] = 0;
        int64_t n = 0;
        while (n < 100) {
            if (next_random() % 2 == 0) {
                memcpy(sequences[p] + n, words[p], (size_t)m);
                n += m;
            } else {
                sequences[p][n++] = (char)('a' + next_random() % kinds);
            }
        }
        sequences[p][n] = 0;
    }
    int64_t total = 0, check = 0;
    for (int p = 0; p < PROBLEMS; p++) {
        int64_t k = max_repeating(sequences[p], words[p]);
        total += k;
        check = (check * 31 + k) % 1000000007;
    }
    printf("%d problems of about 100 letters: answers sum to %lld, checksum %lld\n", PROBLEMS, (long long)total, (long long)check);
    return 0;
}
