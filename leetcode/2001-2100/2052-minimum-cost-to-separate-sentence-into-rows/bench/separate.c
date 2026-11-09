// LeetCode #2052: Minimum Cost to Separate Sentence Into Rows -- C mirror
// of the ★ arm's benchmark (separate.kara): the same 600 sentences, the
// same dynamic programming from the end, the word lengths read off the
// text at each space.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2052;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t minimum_cost(const char *sentence, int64_t len, int64_t k) {
    int64_t *lens = malloc((len + 1) * sizeof(int64_t));
    int64_t n = 0, run = 0;
    for (int64_t i = 0; i <= len; i++) {
        if (i == len || sentence[i] == ' ') {
            lens[n++] = run;
            run = 0;
        } else {
            run++;
        }
    }
    int64_t *best = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t width = -1, least = INT64_MAX, j = i;
        while (j < n && width + 1 + lens[j] <= k) {
            width += 1 + lens[j];
            j++;
            if (j == n) {
                least = 0;
            } else {
                int64_t c = (k - width) * (k - width) + best[j];
                if (c < least) least = c;
            }
        }
        best[i] = least;
    }
    int64_t answer = best[0];
    free(lens);
    free(best);
    return answer;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    char *text = malloc(5100);
    int64_t sum = 0, check = 0;
    for (int64_t t = 0; t < 600; t++) {
        int64_t len = 0;
        while (len < 4990) {
            if (len > 0) text[len++] = ' ';
            int64_t w = next_random() % 10 + 1;
            for (int64_t i = 0; i < w; i++) text[len++] = letters[next_random() % 26];
        }
        int64_t k = 20 + t % 200 * 20;
        int64_t cost = minimum_cost(text, len, k);
        sum += cost;
        check = (check * 31 + cost) % 1000000007;
    }
    free(text);
    printf("600 sentences: sum %lld, checksum %lld\n", (long long)sum, (long long)check);
    return 0;
}
