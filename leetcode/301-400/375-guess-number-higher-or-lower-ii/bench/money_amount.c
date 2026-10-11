// Benchmark for #375 -- mirror of money_amount.kara, with the table as one
// flat allocation of (n + 2) x (n + 2) cells.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t get_money_amount(int64_t n) {
    int64_t w = n + 2;
    int64_t *cost = calloc((size_t)(w * w), sizeof(int64_t));
    for (int64_t len = 2; len <= n; len++) {
        for (int64_t i = 1; i <= n - len + 1; i++) {
            int64_t j = i + len - 1;
            int64_t best = INT64_MAX;
            for (int64_t k = i; k <= j; k++) {
                int64_t left = cost[i * w + k - 1], right = cost[(k + 1) * w + j];
                int64_t worse = left > right ? left : right;
                if (k + worse < best) best = k + worse;
            }
            cost[i * w + j] = best;
        }
    }
    int64_t out = cost[1 * w + n];
    free(cost);
    return out;
}

int main(void) {
    int64_t checksum = 0;
    for (int64_t n = 1; n <= 200; n++) checksum = (checksum * 1009 + get_money_amount(n)) % 1000000007;
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
