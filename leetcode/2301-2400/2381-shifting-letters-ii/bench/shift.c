// LeetCode #2381: Shifting Letters II -- the bench, the ★ arm in C: a
// difference array of the shifts, its running sum each letter's step.
// The difference array and the result are allocated in each call, as the
// other languages' are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 50000

static char *shifting_letters(const char *s, int64_t n, const int64_t (*shifts)[3], int64_t q) {
    int64_t *diff = calloc(n + 1, sizeof(int64_t));
    for (int64_t k = 0; k < q; k++) {
        int64_t step = shifts[k][2] == 1 ? 1 : -1;
        diff[shifts[k][0]] += step;
        diff[shifts[k][1] + 1] -= step;
    }
    char *out = malloc(n + 1);
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += diff[i];
        int64_t letter = ((s[i] - 'a') + total) % 26;
        if (letter < 0) {
            letter += 26;
        }
        out[i] = (char)('a' + letter);
    }
    out[n] = 0;
    free(diff);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char s[N + 1];
static int64_t lists[10][N][3];

int main(void) {
    // a string of 5 * 10^4 letters and 10 lists of 5 * 10^4 shifts, list
    // l's shifts up to 10^l letters long, capped at the string; pass p
    // applies list p % 10
    int64_t seed = 2381;
    for (int i = 0; i < N; i++) {
        s[i] = (char)('a' + next_random(&seed) % 26);
    }
    for (int l = 0; l < 10; l++) {
        int64_t reach = 1;
        for (int k = 0; k < l; k++) {
            reach = reach * 10 < N ? reach * 10 : N;
        }
        for (int i = 0; i < N; i++) {
            int64_t start = next_random(&seed) % N;
            int64_t end = start + next_random(&seed) % reach;
            if (end > N - 1) {
                end = N - 1;
            }
            lists[l][i][0] = start;
            lists[l][i][1] = end;
            lists[l][i][2] = next_random(&seed) % 2;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 200; p++) {
        char *t = shifting_letters(s, N, (const int64_t (*)[3])lists[p % 10], N);
        for (int i = 0; i < N; i++) {
            check = (check * 31 + (t[i] - 'a') + p) % 1000000007;
        }
        free(t);
    }
    printf("200 passes over 5 * 10^4 letters: checksum %lld\n", (long long)check);
    return 0;
}
