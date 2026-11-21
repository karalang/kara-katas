// LeetCode #2416: Sum of Prefix Scores of Strings -- the bench, the ★ arm:
// a trie in flat arrays, node k's child by letter c at `next[26 k + c]`
// and `count[k]` the words through it, both grown by doubling.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LISTS 10
#define WORDS 2000

static int64_t seed = 2416;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    unsigned char *bytes;
    int len;
} Word;

static void sum_prefix_scores(const Word *words, int n, int64_t *scores) {
    size_t cap = 64, len = 1;
    int64_t *next = calloc(26 * cap, sizeof *next);
    int64_t *count = calloc(cap, sizeof *count);
    for (int i = 0; i < n; i++) {
        size_t at = 0;
        for (int k = 0; k < words[i].len; k++) {
            int c = words[i].bytes[k] - 'a';
            if (next[26 * at + c] == 0) {
                if (len == cap) {
                    cap *= 2;
                    next = realloc(next, 26 * cap * sizeof *next);
                    count = realloc(count, cap * sizeof *count);
                }
                memset(next + 26 * len, 0, 26 * sizeof *next);
                count[len] = 0;
                next[26 * at + c] = (int64_t)len;
                len++;
            }
            at = (size_t)next[26 * at + c];
            count[at] += 1;
        }
    }
    for (int i = 0; i < n; i++) {
        size_t at = 0;
        int64_t score = 0;
        for (int k = 0; k < words[i].len; k++) {
            at = (size_t)next[26 * at + (words[i].bytes[k] - 'a')];
            score += count[at];
        }
        scores[i] = score;
    }
    free(next);
    free(count);
}

int main(void) {
    static Word lists[LISTS][WORDS];
    for (int i = 0; i < LISTS; i++) {
        for (int w = 0; w < WORDS; w++) {
            int len = 1 + (int)(next_random() % 50);
            unsigned char *bytes = malloc(len);
            for (int k = 0; k < len; k++) {
                bytes[k] = (unsigned char)('a' + next_random() % (2 + 2 * i));
            }
            lists[i][w].bytes = bytes;
            lists[i][w].len = len;
        }
    }
    int64_t *scores = malloc(WORDS * sizeof *scores);
    int64_t check = 0;
    for (int p = 0; p < 20; p++) {
        for (int i = 0; i < LISTS; i++) {
            sum_prefix_scores(lists[i], WORDS, scores);
            for (int w = 0; w < WORDS; w++) {
                check = (check * 31 + scores[w] + p) % 1000000007;
            }
        }
    }
    printf("20 passes over 10 lists of 2000 words: checksum %lld\n", (long long)check);
    return 0;
}
