// LeetCode #1662 bench: the ★ arm, two cursors, one in each array.
//
// 20 pairs of word arrays spelling texts of 10^6 letters, cut into words
// of about 8 letters, are built first; half spell the same text and half
// differ in the last letter. Then each pair is checked 20 times. Each
// word is its own heap string, as in the other languages.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **text;
    int64_t *len;
    int64_t count;
} Words;

static bool array_strings_are_equal(const Words *word1, const Words *word2) {
    int64_t w1 = 0, i1 = 0, w2 = 0, i2 = 0;
    while (w1 < word1->count && w2 < word2->count) {
        const char *a = word1->text[w1];
        const char *b = word2->text[w2];
        if (a[i1] != b[i2]) return false;
        i1++;
        i2++;
        if (i1 == word1->len[w1]) {
            w1++;
            i1 = 0;
        }
        if (i2 == word2->len[w2]) {
            w2++;
            i2 = 0;
        }
    }
    return w1 == word1->count && w2 == word2->count;
}

static int64_t seed;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void push(Words *w, int64_t *cap, const char *from, int64_t n) {
    if (w->count == *cap) {
        *cap = *cap ? *cap * 2 : 16;
        w->text = realloc(w->text, *cap * sizeof *w->text);
        w->len = realloc(w->len, *cap * sizeof *w->len);
    }
    char *s = malloc(n + 1);
    memcpy(s, from, n);
    s[n] = 0;
    w->text[w->count] = s;
    w->len[w->count] = n;
    w->count++;
}

static Words cut(const char *text, int64_t n) {
    Words w = {0};
    int64_t cap = 0, start = 0;
    for (int64_t i = 1; i < n; i++) {
        if (next_random() % 8 == 0) {
            push(&w, &cap, text + start, i - start);
            start = i;
        }
    }
    push(&w, &cap, text + start, n - start);
    return w;
}

static void release(Words *w) {
    for (int64_t i = 0; i < w->count; i++) free(w->text[i]);
    free(w->text);
    free(w->len);
}

int main(void) {
    enum { PAIRS = 20, LETTERS = 1000000, ROUNDS = 20 };
    seed = 1662;
    Words cases[PAIRS][2];
    char *text = malloc(LETTERS), *other = malloc(LETTERS);
    for (int k = 0; k < PAIRS; k++) {
        for (int64_t i = 0; i < LETTERS; i++) text[i] = (char)('a' + next_random() % 2);
        memcpy(other, text, LETTERS);
        if (k % 2 == 1) other[LETTERS - 1] = other[LETTERS - 1] == 'a' ? 'b' : 'a';
        cases[k][0] = cut(text, LETTERS);
        cases[k][1] = cut(other, LETTERS);
    }
    free(text);
    free(other);
    int64_t equal = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int k = 0; k < PAIRS; k++) {
            bool answer = array_strings_are_equal(&cases[k][0], &cases[k][1]);
            if (answer) equal++;
            check = (check * 31 + (answer ? 2 : 1) + cases[k][0].count + cases[k][1].count + r) % 1000000007;
        }
    }
    printf("%d pairs of %d letters, %d rounds: %lld equal, checksum %lld\n", PAIRS, LETTERS, ROUNDS,
           (long long)equal, (long long)check);
    for (int k = 0; k < PAIRS; k++) {
        release(&cases[k][0]);
        release(&cases[k][1]);
    }
    return 0;
}
