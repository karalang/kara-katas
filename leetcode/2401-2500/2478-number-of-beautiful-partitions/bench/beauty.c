// LeetCode #2478: Number of Beautiful Partitions -- bench, C mirror of
// beauty.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static bool is_prime_digit(int64_t c) { return c == 2 || c == 3 || c == 5 || c == 7; }

static int64_t beautiful_partitions(const int64_t *digits, int64_t n, int64_t k, int64_t min_length) {
    if (!is_prime_digit(digits[0]) || is_prime_digit(digits[n - 1])) return 0;
    bool *cut = malloc((size_t)(n + 1) * sizeof(bool));
    for (int64_t i = 0; i <= n; i++)
        cut[i] = i == n || (i > 0 && !is_prime_digit(digits[i - 1]) && is_prime_digit(digits[i]));
    int64_t *ways = calloc((size_t)(n + 1), sizeof(int64_t));
    ways[0] = 1;
    for (int64_t r = 0; r < k; r++) {
        int64_t *next = calloc((size_t)(n + 1), sizeof(int64_t));
        int64_t running = 0;
        for (int64_t i = min_length; i <= n; i++) {
            int64_t start = i - min_length;
            if (start == 0 || (cut[start] && start < n)) running = (running + ways[start]) % MOD;
            if (cut[i] && i > 0) next[i] = running;
        }
        free(ways);
        ways = next;
    }
    int64_t answer = ways[n];
    free(ways);
    free(cut);
    return answer;
}

static int64_t seed = 2478;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t strings[20][1000];
    for (int t = 0; t < 20; t++) {
        strings[t][0] = 2;
        for (int i = 1; i < 999; i++) strings[t][i] = 1 + next_random() % 9;
        strings[t][999] = 1;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 90; p++) {
        for (int t = 0; t < 20; t++) {
            int64_t k = 1 + check % 100;
            int64_t m = 1 + check % 5;
            check = (check * 31 + beautiful_partitions(strings[t], 1000, k, m) + p) % MOD;
        }
    }
    printf("90 passes over 20 strings of 1000: checksum %lld\n", (long long)check);
    return 0;
}
