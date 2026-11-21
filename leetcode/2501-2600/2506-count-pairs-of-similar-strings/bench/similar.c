// LeetCode #2506: Count Pairs Of Similar Strings -- C mirror of the
// benchmark (similar.kara): the same lists, passes and checksum; the
// masks counted in an open-addressed table of 256 slots, cleared on
// every ask, probed linearly from a multiplicative hash.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 256

static int64_t seed = 2506;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    char *text;
} Word;

static int64_t similar_pairs(Word *const *words, int64_t n) {
    int64_t keys[SLOTS], counts[SLOTS];
    memset(keys, 0, sizeof keys);
    int64_t pairs = 0;
    for (int64_t w = 0; w < n; w++) {
        int64_t mask = 0;
        for (const char *c = words[w]->text; *c; c++) mask |= (int64_t)1 << (*c - 'a');
        uint64_t s = ((uint64_t)(mask + 1) * 0x9e3779b97f4a7c15ULL) >> 56;
        while (keys[s] != 0 && keys[s] != mask + 1) s = (s + 1) & (SLOTS - 1);
        if (keys[s] == 0) {
            keys[s] = mask + 1;
            counts[s] = 0;
        }
        pairs += counts[s];
        counts[s]++;
    }
    return pairs;
}

static Word *random_word(void) {
    int64_t length = next_random() % 100 + 1;
    int64_t letters = next_random() % 4 + 3;
    Word *w = malloc(sizeof(Word));
    w->text = malloc(length + 1);
    for (int64_t i = 0; i < length; i++) w->text[i] = (char)('a' + next_random() % letters);
    w->text[length] = 0;
    return w;
}

int main(void) {
    const int64_t passes = 24;
    static Word *lists[1000][100];
    for (int l = 0; l < 1000; l++)
        for (int i = 0; i < 100; i++) lists[l][i] = random_word();
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int l = 0; l < 1000; l++) {
            int64_t at = check % 100;
            Word *was = lists[l][at];
            Word copy = {strdup(lists[l][(check / 100 + p) % 100]->text)};
            lists[l][at] = &copy;
            check = (check * 31 + similar_pairs(lists[l], 100) + p) % 1000000007;
            free(copy.text);
            lists[l][at] = was;
        }
    }
    printf("%lld passes over 1000 lists of 100 words: checksum %lld\n", (long long)passes, (long long)check);
    for (int l = 0; l < 1000; l++)
        for (int i = 0; i < 100; i++) {
            free(lists[l][i]->text);
            free(lists[l][i]);
        }
    return 0;
}
