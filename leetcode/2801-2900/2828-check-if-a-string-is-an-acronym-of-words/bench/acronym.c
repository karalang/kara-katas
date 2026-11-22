// LeetCode #2828: Check if a String Is an Acronym of Words -- the bench's
// C mirror of the ★ arm: the lengths first, then every word's first byte
// against s's byte at the same place.

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *words[100];
    int count;
    char s[101];
} Case;

static bool is_acronym(char *const *words, int count, const char *s) {
    if ((size_t)count != strlen(s)) return false;
    for (int i = 0; i < count; i++)
        if (words[i][0] != s[i]) return false;
    return true;
}

static long long seed = 2828;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *word(void) {
    int n = (int)(next_random() % 10 + 1);
    char *w = malloc(n + 1);
    for (int i = 0; i < n; i++) w[i] = (char)(97 + next_random() % 3);
    w[n] = 0;
    return w;
}

int main(void) {
    enum { COUNT = 20000, ROUNDS = 100 };
    Case *cases = malloc(COUNT * sizeof *cases);
    for (int c = 0; c < COUNT; c++) {
        cases[c].count = 100;
        for (int i = 0; i < 100; i++) cases[c].words[i] = word();
        for (int i = 0; i < 100; i++) cases[c].s[i] = cases[c].words[i][0];
        cases[c].s[100] = 0;
        if (next_random() % 4 == 0) {
            int at = (int)(next_random() % 100);
            cases[c].s[at] = (char)(97 + next_random() % 3);
        }
    }
    long long yes = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            bool a = is_acronym(cases[c].words, cases[c].count, cases[c].s);
            if (a) yes++;
            check = (check * 31 + (a ? 1 : 0) + r) % 1000000007;
        }
    printf("%d cases of 100 words, %d rounds: %lld true, checksum %lld\n", COUNT, ROUNDS, yes, check);
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < 100; i++) free(cases[c].words[i]);
    free(cases);
    return 0;
}
