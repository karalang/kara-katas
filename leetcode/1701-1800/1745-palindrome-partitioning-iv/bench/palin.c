// LeetCode #1745: Palindrome Partitioning IV -- the bench (palin.kara in
// C): a table of palindromes, then every pair of cuts.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { COUNT = 20, ROUNDS = 5, N = 2000 };

static bool check_partitioning(const char *b, int64_t n) {
    bool *is = calloc((size_t)(n * n), sizeof(bool));
    for (int64_t i = n - 1; i >= 0; i--) {
        for (int64_t j = i; j < n; j++) {
            is[i * n + j] = b[i] == b[j] && (j - i < 2 || is[(i + 1) * n + j - 1]);
        }
    }
    bool found = false;
    for (int64_t i = 1; i < n - 1 && !found; i++) {
        if (is[i - 1]) {
            for (int64_t j = i; j < n - 1; j++) {
                if (is[i * n + j] && is[(j + 1) * n + n - 1]) {
                    found = true;
                    break;
                }
            }
        }
    }
    free(is);
    return found;
}

static int64_t seed = 1745;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char letter(void) { return next_random() % 2 == 0 ? 'a' : 'b'; }

// writes a random palindrome of n letters at out
static void palindrome(int64_t n, char *out) {
    int64_t half = (n + 1) / 2;
    for (int64_t i = 0; i < half; i++) out[i] = letter();
    for (int64_t i = 0; i < n / 2; i++) out[half + i] = out[n / 2 - 1 - i];
}

int main(void) {
    static char strings[COUNT][N + 1];
    for (int k = 0; k < COUNT; k++) {
        if (k % 2 == 0) {
            int64_t a = next_random() % (N - 2) + 1;
            int64_t b = next_random() % (N - a - 1) + 1;
            palindrome(a, strings[k]);
            palindrome(b, strings[k] + a);
            palindrome(N - a - b, strings[k] + a + b);
        } else {
            for (int64_t i = 0; i < N; i++) strings[k][i] = letter();
        }
        strings[k][N] = 0;
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t k = 0; k < COUNT; k++) {
            int64_t bit = check_partitioning(strings[k], N) ? 1 : 0;
            yes += bit;
            check = (check * 3 + bit + k + r) % 1000000007;
        }
    }
    printf("%d strings of %d letters, %d rounds: %lld split, checksum %lld\n", COUNT, N, ROUNDS, (long long)yes, (long long)check);
    return 0;
}
