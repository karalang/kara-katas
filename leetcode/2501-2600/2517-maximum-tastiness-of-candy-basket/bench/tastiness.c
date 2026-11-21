// LeetCode #2517: Maximum Tastiness of Candy Basket -- C mirror of the
// benchmark (tastiness.kara): the same lists, passes, order and checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

static int64_t lists[20][N];
static int64_t sorted[N];

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int fits(int64_t n, int64_t k, int64_t d) {
    int64_t count = 1, last = sorted[0];
    for (int64_t i = 0; i < n; i++) {
        if (sorted[i] - last >= d) {
            count++;
            last = sorted[i];
        }
    }
    return count >= k;
}

static int64_t maximum_tastiness(const int64_t *price, int64_t n, int64_t k) {
    memcpy(sorted, price, n * sizeof(int64_t));
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t lo = 0, hi = (sorted[n - 1] - sorted[0]) / (k - 1);
    while (lo < hi) {
        int64_t mid = lo + (hi - lo + 1) / 2;
        if (fits(n, k, mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}

static int64_t seed = 2517;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t below(int64_t top) {
    int64_t a = next_random();
    int64_t b = next_random();
    return (a * 32768 + b) % top;
}

int main(void) {
    for (int t = 0; t < 20; t++)
        for (int i = 0; i < N; i++) lists[t][i] = below(1000000000) + 1;
    const int64_t passes = 3;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++)
        for (int t = 0; t < 20; t++)
            check = (check * 31 + maximum_tastiness(lists[t], N, check % 1000 + 2) + p) % 1000000007;
    printf("%lld passes over 20 lists of 10^5 prices: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
