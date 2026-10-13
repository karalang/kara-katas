// Benchmark for #474: C mirror of the ★ arm (0/1 knapsack with two
// budgets, one table); see ones_and_zeroes.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t count_zeros(const char *s) {
    int64_t zeros = 0;
    for (const char *p = s; *p; p++) {
        if (*p == '0') {
            zeros++;
        }
    }
    return zeros;
}

static int64_t find_max_form(char **strs, int count, int64_t m, int64_t n) {
    int64_t w = n + 1;
    int64_t *best = calloc((size_t)((m + 1) * w), sizeof(int64_t));
    for (int k = 0; k < count; k++) {
        int64_t zeros = count_zeros(strs[k]);
        int64_t ones = (int64_t)strlen(strs[k]) - zeros;
        for (int64_t i = m; i >= zeros; i--) {
            for (int64_t j = n; j >= ones; j--) {
                int64_t take = best[(i - zeros) * w + (j - ones)] + 1;
                if (take > best[i * w + j]) {
                    best[i * w + j] = take;
                }
            }
        }
    }
    int64_t answer = best[m * w + n];
    free(best);
    return answer;
}

static int64_t seed = 474;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    char *strs[600];
    for (int k = 0; k < 600; k++) {
        int64_t size = 1 + next_random() % 100;
        int64_t lean = next_random() % 3;
        char *s = malloc((size_t)size + 1);
        for (int64_t i = 0; i < size; i++) {
            int64_t r = next_random() % 4;
            int zero = lean == 0 ? r != 0 : lean == 1 ? r == 0 : r < 2;
            s[i] = zero ? '0' : '1';
        }
        s[size] = '\0';
        strs[k] = s;
    }
    int rounds = 300;
    int64_t total = 0;
    int64_t checksum = 0;
    for (int r = 0; r < rounds; r++) {
        int64_t m = 50 + next_random() % 51;
        int64_t n = 50 + next_random() % 51;
        int64_t got = find_max_form(strs, 600, m, n);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    printf("%d rounds on 600 strings: %lld chosen, checksum %lld\n", rounds, (long long)total, (long long)checksum);
    for (int k = 0; k < 600; k++) {
        free(strs[k]);
    }
    return 0;
}
