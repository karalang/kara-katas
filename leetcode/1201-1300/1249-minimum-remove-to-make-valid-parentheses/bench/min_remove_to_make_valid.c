// LeetCode #1249 bench, in C: the ★ arm (a stack of the places of the `(`
// not yet closed, and an array of flags for the characters to keep) on 50
// random strings of 100000 characters built once, each with its own share
// of parentheses, each asked 4 times; every kept string folded into a
// checksum.

#include <stdio.h>

#define N 100000
#define TEXTS 50

static long long seed = 1249;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char keep[N];
static int open_at[N];

static int min_remove_to_make_valid(const char *s, int n, char *out) {
    int top = 0;
    for (int i = 0; i < n; i++) {
        keep[i] = 1;
        if (s[i] == '(') open_at[top++] = i;
        else if (s[i] == ')') {
            if (top == 0) keep[i] = 0;
            else top--;
        }
    }
    for (int k = 0; k < top; k++) keep[open_at[k]] = 0;
    int m = 0;
    for (int i = 0; i < n; i++)
        if (keep[i]) out[m++] = s[i];
    return m;
}

static char texts[TEXTS][N];
static char kept[N];

int main(void) {
    for (int t = 0; t < TEXTS; t++) {
        long long percent = next_random() % 101;
        for (int i = 0; i < N; i++) {
            if (next_random() % 100 < percent) texts[t][i] = next_random() % 2 == 0 ? '(' : ')';
            else texts[t][i] = "abcde"[next_random() % 5];
        }
    }
    long long check = 0;
    for (int r = 0; r < 4; r++)
        for (int t = 0; t < TEXTS; t++) {
            int m = min_remove_to_make_valid(texts[t], N, kept);
            for (int i = 0; i < m; i++) check = (check * 131 + kept[i]) % 1000000007;
        }
    printf("4 rounds of 50 strings of 100000 characters: checksum %lld\n", check);
    return 0;
}
