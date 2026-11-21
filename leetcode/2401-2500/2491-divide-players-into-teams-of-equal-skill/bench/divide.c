// LeetCode #2491: Divide Players Into Teams of Equal Skill -- C mirror of
// the ★ arm's benchmark (divide.kara): the same 20 lists and 25 passes,
// each list copied and sorted by `qsort` for every answer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t sorted[N];

static int64_t divide_players(const int64_t *skill, int64_t n) {
    memcpy(sorted, skill, sizeof(int64_t) * (size_t)n);
    qsort(sorted, (size_t)n, sizeof(int64_t), cmp);
    int64_t target = sorted[0] + sorted[n - 1];
    int64_t chemistry = 0;
    for (int64_t i = 0; i < n / 2; i++) {
        int64_t a = sorted[i], b = sorted[n - 1 - i];
        if (a + b != target) return -1;
        chemistry += a * b;
    }
    return chemistry;
}

static int64_t seed = 2491;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t lists[20][N];

int main(void) {
    const int64_t n = N, passes = 25;
    for (int l = 0; l < 20; l++) {
        int64_t total = 500 + l * 50;
        for (int64_t k = 0; k < n / 2; k++) {
            int64_t a = next_random() % (total - 1) + 1;
            lists[l][2 * k] = a;
            lists[l][2 * k + 1] = total - a;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t hi = next_random();
            int64_t j = (hi * 32768 + next_random()) % (i + 1);
            int64_t t = lists[l][i];
            lists[l][i] = lists[l][j];
            lists[l][j] = t;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int l = 0; l < 20; l++) {
            int64_t at = check % n;
            int64_t was = lists[l][at];
            lists[l][at] = (check / n + p) % 1000 + 1;
            check = (check * 31 + divide_players(lists[l], n) + 1 + p) % 1000000007;
            lists[l][at] = was;
        }
    }
    printf("%lld passes over 20 lists of 10^5: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
