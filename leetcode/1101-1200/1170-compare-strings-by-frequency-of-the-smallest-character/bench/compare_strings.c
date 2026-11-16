// LeetCode #1170: Compare Strings by Frequency of the Smallest Character --
// the ★ arm's bench in C: words counted by frequency, the counts summed
// from the top down, each query answered by one look-up. Each string is a
// NUL-terminated array of 11 chars.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef char Word[11];

static int64_t f(const char *s) {
    int smallest = 'z' + 1;
    int64_t count = 0;
    for (; *s; s++) {
        int b = (unsigned char)*s;
        if (b < smallest) {
            smallest = b;
            count = 1;
        } else if (b == smallest) {
            count++;
        }
    }
    return count;
}

static void num_smaller_by_frequency(const Word *queries, int nq, const Word *words, int nw, int64_t *out) {
    // above[k]: the words whose frequency is at least k
    int64_t above[12] = {0};
    for (int i = 0; i < nw; i++) above[f(words[i])]++;
    for (int k = 10; k >= 0; k--) above[k] += above[k + 1];
    for (int i = 0; i < nq; i++) out[i] = above[f(queries[i]) + 1];
}

static int64_t seed = 1170;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void random_word(char *w, int64_t letters) {
    int64_t n = 1 + next_random() % 10;
    for (int64_t i = 0; i < n; i++) w[i] = (char)('a' + next_random() % letters);
    w[n] = 0;
}

int main(void) {
    const int rounds = 300;
    static const int64_t LETTERS[4] = {2, 3, 5, 26};
    static Word queries[16][2000], words[16][2000];
    static int64_t got[2000];
    for (int l = 0; l < 16; l++) {
        for (int i = 0; i < 2000; i++) random_word(queries[l][i], LETTERS[l % 4]);
        for (int i = 0; i < 2000; i++) random_word(words[l][i], LETTERS[l % 4]);
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int l = 0; l < 16; l++) {
            int64_t i = next_random() % 2000;
            random_word(queries[l][i], LETTERS[l % 4]);
            int64_t j = next_random() % 2000;
            random_word(words[l][j], LETTERS[l % 4]);
            num_smaller_by_frequency(queries[l], 2000, words[l], 2000, got);
            for (int k = 0; k < 2000; k++) {
                total += got[k];
                check = (check * 131 + got[k] + 1) % 1000000007;
            }
        }
    }
    printf("%d rounds over 16 lists of 2000 queries and 2000 words: total %lld, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
