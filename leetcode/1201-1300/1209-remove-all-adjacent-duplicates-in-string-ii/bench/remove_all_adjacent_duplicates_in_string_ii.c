// LeetCode #1209 bench, in C: the ★ arm (a stack of runs, each a letter and
// how many times it has come in a row, a run popped when it reaches `k`)
// on 12 strings of 100000 letters drawn once, then 10 rounds over the
// strings with k = 2, 3 and 4, each answer's length and last letter folded
// into a checksum.

#include <stdio.h>
#include <stdlib.h>

#define TEXTS 12
#define LEN 100000

static long long seed = 1209;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char run_letter[LEN];
static long long run_count[LEN];

// The answer is written to `out`; its length is returned.
static int remove_duplicates(const char *s, int n, long long k, char *out) {
    int top = 0;
    for (int i = 0; i < n; i++) {
        char c = s[i];
        if (top > 0 && run_letter[top - 1] == c) {
            if (++run_count[top - 1] == k) top--;
        } else {
            run_letter[top] = c;
            run_count[top] = 1;
            top++;
        }
    }
    int len = 0;
    for (int r = 0; r < top; r++)
        for (long long j = 0; j < run_count[r]; j++) out[len++] = run_letter[r];
    return len;
}

int main(void) {
    static char texts[TEXTS][LEN];
    static char out[LEN];
    for (int i = 0; i < TEXTS; i++) {
        if (i < 4) {
            for (int j = 0; j < LEN; j++) texts[i][j] = (char)('a' + next_random() % 2);
        } else if (i < 8) {
            for (int j = 0; j < LEN; j++) texts[i][j] = (char)('a' + next_random() % 3);
        } else {
            for (int j = 0; j < LEN / 2; j++) texts[i][j] = (char)('a' + next_random() % 26);
            for (int j = 0; j < LEN / 2; j++) texts[i][LEN - 1 - j] = texts[i][j];
        }
    }
    long long check = 0;
    for (int round = 0; round < 10; round++)
        for (int i = 0; i < TEXTS; i++)
            for (long long k = 2; k < 5; k++) {
                int len = remove_duplicates(texts[i], LEN, k, out);
                long long last = len > 0 ? (unsigned char)out[len - 1] : 0;
                check = (check * 131 + len + last + round) % 1000000007;
            }
    printf("10 rounds over 12 strings of 100000 letters: checksum %lld\n", check);
    return 0;
}
