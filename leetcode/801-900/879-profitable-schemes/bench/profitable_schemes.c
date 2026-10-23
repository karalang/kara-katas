// LeetCode #879 bench: C mirror of profitable_schemes.kara (the ★ arm, a
// knapsack over members and profit) on the same 600 cases.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t profitable_schemes(int64_t n, int64_t min_profit, const int64_t *group, const int64_t *profit, int64_t crimes) {
    const int64_t modulus = 1000000007;
    int64_t **ways = malloc((size_t)(n + 1) * sizeof *ways);
    for (int64_t m = 0; m <= n; m++) {
        ways[m] = calloc((size_t)(min_profit + 1), sizeof **ways);
    }
    ways[0][0] = 1;
    for (int64_t c = 0; c < crimes; c++) {
        int64_t g = group[c];
        int64_t gain = profit[c];
        for (int64_t m = n; m >= g; m--) {
            for (int64_t p = 0; p <= min_profit; p++) {
                int64_t q = p + gain < min_profit ? p + gain : min_profit;
                ways[m][q] = (ways[m][q] + ways[m - g][p]) % modulus;
            }
        }
    }
    int64_t total = 0;
    for (int64_t m = 0; m <= n; m++) {
        total = (total + ways[m][min_profit]) % modulus;
    }
    for (int64_t m = 0; m <= n; m++) {
        free(ways[m]);
    }
    free(ways);
    return total;
}

static int64_t seed = 879;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t total = 0, check = 0;
    int64_t group[100], profit[100];
    for (int k = 0; k < 600; k++) {
        int64_t n = 50 + next_random() % 51;
        int64_t min_profit = 50 + next_random() % 51;
        int wide = k % 2 == 0;
        for (int c = 0; c < 100; c++) {
            group[c] = next_random() % (wide ? 100 : 10) + 1;
            profit[c] = next_random() % (wide ? 101 : 11);
        }
        int64_t answer = profitable_schemes(n, min_profit, group, profit, 100);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    printf("600 cases of 100 crimes: counts sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
