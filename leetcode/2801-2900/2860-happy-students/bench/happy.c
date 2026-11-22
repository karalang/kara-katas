// LeetCode #2860: Happy Students -- the bench: the ★ arm over 50
// classes of 10^5 students, LeetCode's most, half of them random and
// half built around a group size, all drawn first, then each answered 20
// times, the sort included.
// C sorts with the C library's `qsort`, where the others use their
// languages' own sorts.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t count_ways(const int64_t *nums, int64_t n, int64_t *sorted) {
    memcpy(sorted, nums, sizeof(int64_t) * n);
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t ways = 0;
    for (int64_t k = 0; k <= n; k++) {
        int chosen_ok = k == 0 || sorted[k - 1] < k;
        int left_ok = k == n || sorted[k] > k;
        if (chosen_ok && left_ok) ways++;
    }
    return ways;
}

static int64_t seed = 2860;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}
static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }
static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static void class(int64_t n, int64_t *nums) {
    if (next_random() % 2 == 0) {
        for (int64_t i = 0; i < n; i++) nums[i] = wide() % n;
        return;
    }
    int64_t g = wide() % (n + 1);
    for (int64_t i = 0; i < n; i++) {
        int64_t x = i < g ? wide() % max64(g, 1) : g + 1 + wide() % max64(n - g, 1);
        nums[i] = min64(x, n - 1);
    }
    if (next_random() % 4 == 0) {
        int64_t at = wide() % n;
        nums[at] = min64(g, n - 1);
    }
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = wide() % (i + 1);
        int64_t t = nums[i];
        nums[i] = nums[j];
        nums[j] = t;
    }
}

int main(void) {
    const int64_t count = 50, rounds = 20, n = 100000;
    int64_t *classes = malloc(sizeof(int64_t) * count * n), *sorted = malloc(sizeof(int64_t) * n);
    for (int64_t c = 0; c < count; c++) class(n, classes + c * n);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t ways = count_ways(classes + c * n, n, sorted);
            total += ways;
            check = (check * 31 + ways + r) % 1000000007;
        }
    }
    printf("%lld classes of %lld, %lld rounds: %lld ways, checksum %lld\n", (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(classes);
    free(sorted);
    return 0;
}
