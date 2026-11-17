// LeetCode #2223: Sum of Scores of Built Strings -- bench mirror of
// scores.kara: the Z-function by the Z-algorithm, z[0] = n, summed.
#include <stdio.h>
#include <string.h>

#define A 20
#define N 100000

static long z[N];

static long sum_scores(const char *s, long n) {
    z[0] = n;
    long l = 0, r = 0;
    for (long i = 1; i < n; i++) {
        z[i] = 0;
        if (i < r) z[i] = r - i < z[i - l] ? r - i : z[i - l];
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > r) {
            l = i;
            r = i + z[i];
        }
    }
    long total = 0;
    for (long i = 0; i < n; i++) total += z[i];
    return total;
}

static long seed = 2223;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char letter(void) { return next_random() % 2 == 1 ? 'b' : 'a'; }

static char words[A][N];
static char s[N + 1];

int main(void) {
    // 10^5 letters, each 'a' or 'b'
    for (int a = 0; a < A; a++)
        for (long i = 0; i < N; i++) words[a][i] = letter();
    long check = 0;
    for (int a = 0; a < A; a++)
        for (long r = 0; r < 5; r++) {
            // punch: one letter is drawn again before each answer
            words[a][r * 19999] = letter();
            memcpy(s, words[a], N);
            s[N] = 0;
            check = (check * 31 + sum_scores(s, N)) % 1000000007;
        }
    printf("20 strings of 10^5, 5 punches: checksum %ld\n", check);
    return 0;
}
