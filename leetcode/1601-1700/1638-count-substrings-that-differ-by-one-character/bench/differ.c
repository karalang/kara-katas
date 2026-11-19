// LeetCode #1638: Count Substrings That Differ by One Character -- the
// bench's C mirror: the ★ arm on 5000 random pairs of 100-letter words
// over the letters a to c, all drawn first, the two run tables allocated
// per call as the other languages' are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { PAIRS = 5000, LEN = 100 };

static int64_t count_substrings(const char *s, const char *t) {
    size_t n = strlen(s), m = strlen(t), w = m + 1;
    int64_t *left = calloc((n + 1) * w, sizeof(int64_t));
    int64_t *right = calloc((n + 1) * w, sizeof(int64_t));
    for (size_t i = 0; i < n; i++)
        for (size_t j = 0; j < m; j++)
            if (s[i] == t[j]) left[(i + 1) * w + j + 1] = left[i * w + j] + 1;
    for (size_t i = n; i-- > 0;)
        for (size_t j = m; j-- > 0;)
            if (s[i] == t[j]) right[i * w + j] = right[(i + 1) * w + j + 1] + 1;
    int64_t count = 0;
    for (size_t i = 0; i < n; i++)
        for (size_t j = 0; j < m; j++)
            if (s[i] != t[j]) count += (left[i * w + j] + 1) * (right[(i + 1) * w + j + 1] + 1);
    free(left);
    free(right);
    return count;
}

static int64_t seed = 1638;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void random_word(char *word) {
    for (int i = 0; i < LEN; i++) word[i] = (char)('a' + next_random() % 3);
    word[LEN] = 0;
}

int main(void) {
    static char words[PAIRS][2][LEN + 1];
    for (int p = 0; p < PAIRS; p++) {
        random_word(words[p][0]);
        random_word(words[p][1]);
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < PAIRS; p++) {
        int64_t count = count_substrings(words[p][0], words[p][1]);
        total += count;
        check = (check * 31 + count + 1) % 1000000007;
    }
    printf("5000 pairs of 100 letters: counts sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
