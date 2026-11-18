// LeetCode #2318: Number of Distinct Roll Sequences -- the bench, the ★
// arm in C. The count of sequences ending in each pair of rolls, a 6 by
// 6 table rolled forward once per roll, each next roll coprime with the
// last and unlike the last two. O(216 n).

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

static int64_t distinct_sequences(int64_t n) {
    const int64_t modulus = 1000000007;
    if (n == 1)
        return 6;
    int64_t ends[6][6], next[6][6];
    for (int a = 0; a < 6; a++)
        for (int b = 0; b < 6; b++)
            ends[a][b] = (a != b && gcd(a + 1, b + 1) == 1) ? 1 : 0;
    for (int64_t r = 2; r < n; r++) {
        memset(next, 0, sizeof next);
        for (int a = 0; a < 6; a++)
            for (int b = 0; b < 6; b++)
                if (ends[a][b] > 0)
                    for (int c = 0; c < 6; c++)
                        if (c != a && c != b && gcd(b + 1, c + 1) == 1)
                            next[b][c] = (next[b][c] + ends[a][b]) % modulus;
        memcpy(ends, next, sizeof ends);
    }
    int64_t total = 0;
    for (int a = 0; a < 6; a++)
        for (int b = 0; b < 6; b++)
            total = (total + ends[a][b]) % modulus;
    return total;
}

int main(void) {
    int64_t check = 0;
    for (int64_t p = 0; p < 5; p++)
        for (int64_t n = 9981; n <= 10000; n++)
            check = (check * 31 + distinct_sequences(n) + p) % 1000000007;
    printf("5 passes over 20 counts of rolls up to 10^4: checksum %lld\n", (long long)check);
    return 0;
}
