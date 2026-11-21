// LeetCode #2451: Odd String Difference -- the bench, the ★ arm: the
// common difference array read off the first three words, and the word
// whose array is not it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *steps;
    int64_t length;
} Steps;

// a fresh array of the word's steps, as each arm's vector is
static Steps differences(const char *word) {
    int64_t n = (int64_t)strlen(word);
    Steps s = {malloc((n > 1 ? n - 1 : 1) * sizeof(int64_t)), n - 1};
    for (int64_t j = 1; j < n; j++) s.steps[j - 1] = (int64_t)word[j] - (int64_t)word[j - 1];
    return s;
}

static int same(Steps a, Steps b) {
    return a.length == b.length && memcmp(a.steps, b.steps, a.length * sizeof(int64_t)) == 0;
}

static const char *odd_string(char **words, int64_t m) {
    Steps a = differences(words[0]), b = differences(words[1]), c = differences(words[2]);
    Steps common = same(a, b) || same(a, c) ? a : b;
    const char *answer = words[0];
    for (int64_t i = 0; i < m; i++) {
        Steps d = differences(words[i]);
        int differs = !same(d, common);
        free(d.steps);
        if (differs) {
            answer = words[i];
            break;
        }
    }
    free(a.steps);
    free(b.steps);
    free(c.steps);
    return answer;
}

static int64_t seed = 2451;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *word_of(const int64_t *steps) {
    int64_t at = 0, low = 0, high = 0;
    for (int j = 0; j < 19; j++) {
        at += steps[j];
        if (at < low) low = at;
        if (at > high) high = at;
    }
    int64_t code = -low + next_random() % (26 - (high - low));
    char *w = malloc(21);
    w[0] = (char)(97 + code);
    for (int j = 0; j < 19; j++) {
        code += steps[j];
        w[j + 1] = (char)(97 + code);
    }
    w[20] = 0;
    return w;
}

int main(void) {
    char ***lists = malloc(2000 * sizeof(char **));
    for (int c = 0; c < 2000; c++) {
        int64_t common[19], other[19];
        for (int j = 0; j < 19; j++) common[j] = next_random() % 3 - 1;
        memcpy(other, common, sizeof(common));
        other[18] += 1;
        int64_t odd = next_random() % 100;
        lists[c] = malloc(100 * sizeof(char *));
        for (int i = 0; i < 100; i++) lists[c][i] = word_of(i == odd ? other : common);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 110; p++)
        for (int64_t c = 0; c < 2000; c++) {
            char **words = lists[c];
            int64_t j = (p + c) % 100;
            char *t = words[0];
            words[0] = words[j];
            words[j] = t;
            const char *answer = odd_string(words, 100);
            for (const char *x = answer; *x; x++) check = (check * 31 + (int64_t)*x + p) % 1000000007;
        }
    printf("110 passes over 2000 lists of 100 words: checksum %lld\n", (long long)check);
    for (int c = 0; c < 2000; c++) {
        for (int i = 0; i < 100; i++) free(lists[c][i]);
        free(lists[c]);
    }
    free(lists);
    return 0;
}
