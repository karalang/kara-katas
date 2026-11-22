// LeetCode #2788: Split Strings by Separator -- the bench in C: the ★ arm
// over 20000 lists of 100 words of 20 characters from a, b, c and the six
// separators, each split by one of them, all drawn first, then each
// answered 10 times, every piece copied into a fresh buffer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20000
#define WORDS 100
#define LEN 20

static int64_t seed = 2788;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    char *text;
    int64_t len;
} Piece;

static int64_t split_words_by_separator(char words[WORDS][LEN], char separator, Piece *out) {
    int64_t m = 0;
    for (int w = 0; w < WORDS; w++) {
        int64_t start = 0;
        for (int64_t i = 0; i <= LEN; i++) {
            if (i == LEN || words[w][i] == separator) {
                if (i > start) {
                    char *t = malloc(i - start);
                    memcpy(t, words[w] + start, i - start);
                    out[m].text = t;
                    out[m].len = i - start;
                    m++;
                }
                start = i + 1;
            }
        }
    }
    return m;
}

static char cases[COUNT][WORDS][LEN];
static char seps[COUNT];
static Piece got[WORDS * LEN];

int main(void) {
    int rounds = 10;
    const char *letters = "abc.,|$#@";
    const char *separators = ".,|$#@";
    for (int c = 0; c < COUNT; c++) {
        for (int w = 0; w < WORDS; w++)
            for (int i = 0; i < LEN; i++) cases[c][w][i] = letters[next_random() % 9];
        seps[c] = separators[next_random() % 6];
    }
    int64_t pieces = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t m = split_words_by_separator(cases[c], seps[c], got);
            pieces += m;
            for (int64_t k = 0; k < m; k++) {
                check = (check * 31 + got[k].len + r) % 1000000007;
                free(got[k].text);
            }
        }
    }
    printf("%d lists of 100 words, %d rounds: %lld pieces, checksum %lld\n", COUNT, rounds, (long long)pieces, (long long)check);
    return 0;
}
