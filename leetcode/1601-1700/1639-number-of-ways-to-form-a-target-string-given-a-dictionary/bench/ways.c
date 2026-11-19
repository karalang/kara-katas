// LeetCode #1639: Number of Ways to Form a Target String Given a
// Dictionary -- the bench's C mirror: the ★ arm on 40 random dictionaries
// of 1000 words of 1000 letters and targets of 500 letters, all over the
// letters a to e and drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { CASES = 40, WORDS = 1000, LEN = 1000, TARGET = 500 };
static const int64_t MODULUS = 1000000007;

static int64_t num_ways(char **words, size_t n, const char *target) {
    size_t length = strlen(words[0]), t = strlen(target);
    int64_t *ways = calloc(t + 1, sizeof(int64_t));
    ways[0] = 1;
    for (size_t column = 0; column < length; column++) {
        int64_t count[26] = {0};
        for (size_t w = 0; w < n; w++) count[words[w][column] - 'a']++;
        size_t top = column + 1 < t ? column + 1 : t;
        for (size_t i = top; i-- > 0;) {
            int64_t have = count[target[i] - 'a'];
            ways[i + 1] = (ways[i + 1] + ways[i] * have) % MODULUS;
        }
    }
    int64_t answer = ways[t];
    free(ways);
    return answer;
}

static int64_t seed = 1639;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *random_word(size_t length) {
    char *word = malloc(length + 1);
    for (size_t i = 0; i < length; i++) word[i] = (char)('a' + next_random() % 5);
    word[length] = 0;
    return word;
}

int main(void) {
    static char *words[CASES][WORDS], *targets[CASES];
    for (int c = 0; c < CASES; c++) {
        for (int w = 0; w < WORDS; w++) words[c][w] = random_word(LEN);
        targets[c] = random_word(TARGET);
    }
    int64_t check = 0;
    for (int c = 0; c < CASES; c++) {
        int64_t ways = num_ways(words[c], WORDS, targets[c]);
        check = (check * 31 + ways + 1) % 1000000007;
    }
    for (int c = 0; c < CASES; c++) {
        for (int w = 0; w < WORDS; w++) free(words[c][w]);
        free(targets[c]);
    }
    printf("40 dictionaries of 1000 words: checksum %lld\n", (long long)check);
    return 0;
}
