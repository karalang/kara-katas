// LeetCode #727: Minimum Window Subsequence -- forward, then back.
// Benchmark mirror of the Kara star arm: walk s1 forward matching s2 in
// order, walk back from where the last letter matched to find the
// latest start, keep the window if shorter, and begin again one place
// after its start. The window is copied out, as the Kara program's
// slice is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *random_word(int64_t n, int64_t kinds, int64_t *seed) {
    char *s = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) s[i] = 'a' + next_random(seed) % kinds;
    s[n] = 0;
    return s;
}

static char *min_window(const char *a, int64_t n, const char *b, int64_t m) {
    int64_t best_start = -1, best_len = n + 1;
    int64_t i = 0;
    while (i < n) {
        int64_t j = 0;
        while (i < n) {
            if (a[i] == b[j]) {
                j++;
                if (j == m) break;
            }
            i++;
        }
        if (j < m) break;
        int64_t end = i, k = m - 1, p = end;
        while (k >= 0) {
            if (a[p] == b[k]) k--;
            p--;
        }
        int64_t start = p + 1;
        if (end - start + 1 < best_len) {
            best_len = end - start + 1;
            best_start = start;
        }
        i = start + 1;
    }
    int64_t len = best_start < 0 ? 0 : best_len;
    char *w = malloc(len + 1);
    if (len > 0) memcpy(w, a + best_start, len);
    w[len] = 0;
    return w;
}

int main(void) {
    int64_t seed = 727;
    char *texts[10];
    for (int d = 0; d < 10; d++) texts[d] = random_word(20000, 8, &seed);
    int64_t sum = 0;
    for (int r = 0; r < 300; r++)
        for (int d = 0; d < 10; d++) {
            char *word = random_word(20, 8, &seed);
            char *w = min_window(texts[d], 20000, word, 20);
            sum += strlen(w);
            free(w);
            free(word);
        }
    printf("300 rounds of 10 texts of 20000 letters: sum %lld\n", (long long)sum);
    for (int d = 0; d < 10; d++) free(texts[d]);
    return 0;
}
