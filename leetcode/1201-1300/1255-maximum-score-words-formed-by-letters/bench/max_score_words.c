// LeetCode #1255 bench, in C: the ★ arm (backtracking, every word in turn
// left out or, when the letters on hand cover it, taken) on 100 random
// cases built once, each 14 words of 1 to 15 letters and 100 letters to
// spend from the first 6 letters of the alphabet; each asked 3 times,
// every best score folded into a checksum.

#include <stdio.h>

#define CASES 100
#define WORDS 14

static long long seed = 1255;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long best(int i, int n, long long words[][26], long long *left, const long long *score) {
    if (i == n) return 0;
    long long top = best(i + 1, n, words, left, score);
    long long need[26];
    for (int c = 0; c < 26; c++) need[c] = words[i][c];
    int fits = 1;
    for (int c = 0; c < 26; c++)
        if (need[c] > left[c]) {
            fits = 0;
            break;
        }
    if (fits) {
        for (int c = 0; c < 26; c++) left[c] -= need[c];
        long long gain = 0;
        for (int c = 0; c < 26; c++) gain += need[c] * score[c];
        long long with = gain + best(i + 1, n, words, left, score);
        if (with > top) top = with;
        for (int c = 0; c < 26; c++) left[c] += need[c];
    }
    return top;
}

static long long max_score_words(char words[][16], int n, const char *letters, int pool, const long long *score) {
    long long counts[WORDS][26] = {{0}};
    for (int w = 0; w < n; w++)
        for (const char *p = words[w]; *p; p++) counts[w][*p - 'a']++;
    long long left[26] = {0};
    for (int k = 0; k < pool; k++) left[letters[k] - 'a']++;
    return best(0, n, counts, left, score);
}

static char words[CASES][WORDS][16];
static char letters[CASES][100];
static long long scores[CASES][26];

int main(void) {
    for (int t = 0; t < CASES; t++) {
        for (int w = 0; w < WORDS; w++) {
            int n = next_random() % 15 + 1;
            for (int k = 0; k < n; k++) words[t][w][k] = 'a' + next_random() % 6;
            words[t][w][n] = 0;
        }
        for (int k = 0; k < 100; k++) letters[t][k] = 'a' + next_random() % 6;
        for (int c = 0; c < 26; c++) scores[t][c] = next_random() % 11;
    }
    long long check = 0;
    for (int r = 0; r < 3; r++)
        for (int t = 0; t < CASES; t++)
            check = (check * 131 + max_score_words(words[t], WORDS, letters[t], 100, scores[t])) % 1000000007;
    printf("3 rounds of 100 cases of 14 words: checksum %lld\n", check);
    return 0;
}
