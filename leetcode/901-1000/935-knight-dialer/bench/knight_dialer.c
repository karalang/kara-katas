// LeetCode #935: Knight Dialer -- bench: counts by last digit, one jump
// at a time. Mirrors knight_dialer.kara, .rs, .py and go-seq/. The jumps
// are a table of up to three per digit with a length beside it.

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static const int JUMPS[10][3] = {{4, 6, 0}, {6, 8, 0}, {7, 9, 0}, {4, 8, 0}, {0, 3, 9},
                                 {0, 0, 0}, {0, 1, 7}, {2, 6, 0}, {1, 3, 0}, {2, 4, 0}};
static const int LENS[10] = {2, 2, 2, 2, 3, 0, 3, 2, 2, 2};

static int64_t knight_dialer(int64_t n) {
    const int64_t modulus = 1000000007;
    int64_t counts[10];
    int64_t next[10];
    for (int d = 0; d < 10; d++) {
        counts[d] = 1;
    }
    for (int64_t step = 1; step < n; step++) {
        for (int d = 0; d < 10; d++) {
            next[d] = 0;
            for (int k = 0; k < LENS[d]; k++) {
                next[d] = (next[d] + counts[JUMPS[d][k]]) % modulus;
            }
        }
        memcpy(counts, next, sizeof(counts));
    }
    int64_t total = 0;
    for (int d = 0; d < 10; d++) {
        total = (total + counts[d]) % modulus;
    }
    return total;
}

int main(void) {
    int64_t rounds = 20;
    int64_t low = 4901;
    int64_t high = 5000;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round counts every length from low to high, starting from a
        // different one
        for (int64_t i = 0; i < high - low + 1; i++) {
            int64_t n = low + (r + i) % (high - low + 1);
            int64_t a = knight_dialer(n);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%lld rounds over n from %lld to %lld: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)low, (long long)high, (long long)total, (long long)check);
    return 0;
}
