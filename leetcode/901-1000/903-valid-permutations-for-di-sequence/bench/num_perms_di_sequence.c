// LeetCode #903: Valid Permutations for DI Sequence -- bench program, C.
//
// Ranks of the last number with running sums, over one string of 4,000
// random letters built once. Each round counts its valid permutations,
// folds the count into a checksum and flips one letter.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t num_perms_di_sequence(const char *s) {
    int64_t m = 1000000007;
    int64_t n = (int64_t)strlen(s);
    int64_t *ways = malloc(sizeof(int64_t));
    ways[0] = 1;
    for (int64_t i = 1; i <= n; i++) {
        int64_t *below = calloc(i + 1, sizeof(int64_t));
        for (int64_t k = 0; k < i; k++) {
            below[k + 1] = (below[k] + ways[k]) % m;
        }
        int64_t *next = calloc(i + 1, sizeof(int64_t));
        for (int64_t j = 0; j <= i; j++) {
            next[j] = s[i - 1] == 'I' ? below[j] : (below[i] - below[j] + m) % m;
        }
        free(below);
        free(ways);
        ways = next;
    }
    int64_t total = 0;
    for (int64_t j = 0; j <= n; j++) {
        total = (total + ways[j]) % m;
    }
    free(ways);
    return total;
}

static int64_t seed = 903;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t length = 4000;
    int64_t rounds = 12;
    char *letters = malloc(length + 1);
    for (int64_t i = 0; i < length; i++) {
        letters[i] = next_random() % 2 == 0 ? 'D' : 'I';
    }
    letters[length] = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t got = num_perms_di_sequence(letters);
        check = (check * 31 + got) % 1000000007;
        int64_t at = r * 7919 % length;
        letters[at] = letters[at] == 'D' ? 'I' : 'D';
    }
    printf("%lld rounds over %lld letters: checksum %lld\n", (long long)rounds, (long long)length,
           (long long)check);
    free(letters);
    return 0;
}
