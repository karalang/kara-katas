// LeetCode #2499: Minimum Total Cost to Make Arrays Unequal -- C mirror of
// the benchmark (unequal.kara): the same pairs, passes and checksum; the
// count per value in a calloc'd array on every ask.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2499;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t minimum_total_cost(const int64_t *nums1, const int64_t *nums2, int64_t n) {
    int64_t *count = calloc(n + 1, sizeof(int64_t));
    int64_t equal = 0, cost = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums1[i] == nums2[i]) {
            count[nums1[i]]++;
            equal++;
            cost += i;
        }
    }
    int64_t mode = 0;
    for (int64_t v = 1; v <= n; v++) {
        if (count[v] > count[mode]) mode = v;
    }
    int64_t shortfall = 2 * count[mode] - equal;
    for (int64_t j = 0; j < n && shortfall > 0; j++) {
        if (nums1[j] != nums2[j] && nums1[j] != mode && nums2[j] != mode) {
            cost += j;
            shortfall--;
        }
    }
    free(count);
    return shortfall > 0 ? -1 : cost;
}

int main(void) {
    const int64_t n = 100000, passes = 33;
    int64_t *firsts[20], *seconds[20];
    for (int q = 0; q < 20; q++) {
        firsts[q] = malloc(n * sizeof(int64_t));
        seconds[q] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            int64_t a = next_random() % 4 + 1;
            firsts[q][i] = a;
            seconds[q][i] = next_random() % 2 == 0 ? a : next_random() % 4 + 1;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int q = 0; q < 20; q++) {
            int64_t at = check % n;
            int64_t was = seconds[q][at];
            seconds[q][at] = (check / n + p) % 2 == 0 ? firsts[q][at] : check % 4 + 1;
            check = (check * 31 + minimum_total_cost(firsts[q], seconds[q], n) + 1 + p) % 1000000007;
            seconds[q][at] = was;
        }
    }
    printf("%lld passes over 20 pairs of 10^5: checksum %lld\n", (long long)passes, (long long)check);
    for (int q = 0; q < 20; q++) { free(firsts[q]); free(seconds[q]); }
    return 0;
}
