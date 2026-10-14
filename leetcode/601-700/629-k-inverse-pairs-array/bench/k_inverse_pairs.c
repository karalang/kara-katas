// LeetCode #629: K Inverse Pairs Array -- C mirror of the Kāra bench.
//
// The ★ arm's rolling DP with a window sum over the same inputs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t k_inverse_pairs(int64_t n, int64_t k) {
    const int64_t modulus = 1000000007;
    int64_t *row = calloc(k + 1, sizeof(int64_t));
    row[0] = 1;
    for (int64_t i = 2; i <= n; i++) {
        int64_t *next = calloc(k + 1, sizeof(int64_t));
        int64_t window = 0;
        for (int64_t j = 0; j <= k; j++) {
            window = (window + row[j]) % modulus;
            if (j >= i) {
                window = (window - row[j - i] + modulus) % modulus;
            }
            next[j] = window;
        }
        free(row);
        row = next;
    }
    int64_t answer = row[k];
    free(row);
    return answer;
}

int main(void) {
    enum { ROUNDS = 100 };
    int64_t checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t n = 500 + (r * 37) % 501;
        int64_t k = 500 + (r * 91) % 501;
        int64_t c = k_inverse_pairs(n, k);
        checksum = (checksum * 31 + c) % 1000000007;
    }
    printf("%d rounds: checksum %lld\n", ROUNDS, (long long)checksum);
    return 0;
}
