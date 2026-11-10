// LeetCode #2100: Find Good Days to Rob the Bank -- C mirror of the ★ arm's
// benchmark (good_days.kara): the same 100 schedules of 10^5 days, the two
// runs counted in two passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t good_days_to_rob_bank(const int64_t *security, int64_t n, int64_t time, int64_t *out) {
    int64_t *before = calloc(n, sizeof *before);
    int64_t *after = calloc(n, sizeof *after);
    for (int64_t i = 1; i < n; i++)
        if (security[i] <= security[i - 1]) before[i] = before[i - 1] + 1;
    for (int64_t i = n - 2; i >= 0; i--)
        if (security[i] <= security[i + 1]) after[i] = after[i + 1] + 1;
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++)
        if (before[i] >= time && after[i] >= time) out[count++] = i;
    free(before);
    free(after);
    return count;
}

static int64_t seed = 2100;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { N = 100000 };
    int64_t total = 0, check = 0;
    for (int r = 0; r < 100; r++) {
        int64_t *security = malloc(N * sizeof *security);
        int64_t *good = malloc(N * sizeof *good);
        int64_t guards = 50000;
        for (int i = 0; i < N; i++) {
            guards += next_random() % 3 - 1;
            if (guards < 0) guards = 0;
            if (guards > 100000) guards = 100000;
            security[i] = guards;
        }
        int64_t time = next_random() % 8;
        int64_t count = good_days_to_rob_bank(security, N, time, good);
        total += count;
        for (int64_t j = 0; j < count; j++) check = (check * 31 + good[j] + 1) % 1000000007;
        free(security);
        free(good);
    }
    printf("100 answers: %lld good days, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
