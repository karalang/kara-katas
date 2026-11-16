// LeetCode #1176: Diet Plan Performance -- the ★ arm's bench in C: one
// window of k days slid across the plan, its sum kept as it goes, each
// window scored as it is reached. The same plan and the same 2000 calls.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t diet_plan_performance(const int64_t *calories, int64_t n, int64_t k, int64_t lower, int64_t upper) {
    int64_t points = 0, total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += calories[i];
        if (i >= k) total -= calories[i - k];
        if (i >= k - 1) {
            if (total < lower) points -= 1;
            else if (total > upper) points += 1;
        }
    }
    return points;
}

static int64_t seed = 1176;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t n = 100000;
    int64_t *calories = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) calories[i] = next_random() % 20001;
    int calls = 2000;
    int64_t check = 0;
    for (int c = 0; c < calls; c++) {
        int64_t k = 1 + next_random() % 100000;
        int64_t mean = 10000 * k;
        int64_t spread = next_random() % 100 * k;
        int64_t p = diet_plan_performance(calories, n, k, mean - spread, mean + spread);
        check = (check * 131 + p + 100000) % 1000000007;
    }
    printf("%d calls: checksum %lld\n", calls, (long long)check);
    free(calories);
    return 0;
}
