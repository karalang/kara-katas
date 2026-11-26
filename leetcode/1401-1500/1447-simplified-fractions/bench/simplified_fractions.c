// LeetCode #1447 Simplified Fractions: the bench, a mirror of
// simplified_fractions.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }

// every numerator below every denominator up to n, kept when the two share
// no factor, in a growing array of strings
static char **simplified_fractions(int n, int *count) {
    int cap = 8, len = 0;
    char **fractions = malloc(cap * sizeof *fractions);
    for (int d = 2; d <= n; d++) {
        for (int a = 1; a < d; a++) {
            if (gcd(a, d) == 1) {
                if (len == cap) {
                    cap *= 2;
                    fractions = realloc(fractions, cap * sizeof *fractions);
                }
                char buf[16];
                int k = snprintf(buf, sizeof buf, "%d/%d", a, d);
                fractions[len] = malloc(k + 1);
                memcpy(fractions[len], buf, k + 1);
                len++;
            }
        }
    }
    *count = len;
    return fractions;
}

int main(void) {
    // every n from 1 to 100, 100 times over, each answer's letters counted
    // and folded to a checksum
    int64_t check = 0;
    for (int r = 0; r < 100; r++) {
        for (int n = 1; n <= 100; n++) {
            int count;
            char **fractions = simplified_fractions(n, &count);
            int64_t letters = 0;
            for (int i = 0; i < count; i++) {
                letters += (int64_t)strlen(fractions[i]);
                free(fractions[i]);
            }
            free(fractions);
            check = (check * 131 + letters) % 1000000007;
        }
    }
    printf("10000 answers: checksum %lld\n", (long long)check);
    return 0;
}
