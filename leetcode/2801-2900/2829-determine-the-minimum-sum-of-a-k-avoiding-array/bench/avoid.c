// LeetCode #2829: Determine the Minimum Sum of a k-avoiding Array -- the
// bench's C mirror of the ★ arm: the numbers walked up from 1, each
// taken unless its partner k - v was taken before it.

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

static long long minimum_sum(long long n, long long k) {
    bool *taken = calloc(n + k + 1, sizeof *taken);
    long long count = 0, sum = 0, v = 1;
    while (count < n) {
        if (v >= k || !taken[k - v]) {
            taken[v] = true;
            count++;
            sum += v;
        }
        v++;
    }
    free(taken);
    return sum;
}

int main(void) {
    const int rounds = 2000;
    long long total = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int n = 1; n <= 50; n++)
            for (int k = 1; k <= 50; k++) {
                long long a = minimum_sum(n, k);
                total += a;
                check = (check * 31 + a + r) % 1000000007;
            }
    printf("2500 pairs, %d rounds: sums total %lld, checksum %lld\n", rounds, total, check);
    return 0;
}
