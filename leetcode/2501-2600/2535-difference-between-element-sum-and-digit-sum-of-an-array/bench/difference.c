// LeetCode #2535 bench, C mirror of difference.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t seed = 2535;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t difference_of_sum(const int64_t *nums, int64_t n) {
    int64_t element_sum = 0, digit_sum = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        element_sum += x;
        int64_t rest = x;
        while (rest > 0) {
            digit_sum += rest % 10;
            rest /= 10;
        }
    }
    int64_t d = element_sum - digit_sum;
    return d < 0 ? -d : d;
}

int main(void) {
    const int64_t passes = 1000, n = 2000;
    static int64_t lists[50][2000];
    for (int q = 0; q < 50; q++)
        for (int64_t i = 0; i < n; i++) lists[q][i] = next_random() % 2000 + 1;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int q = 0; q < 50; q++) {
            int64_t at = check % n;
            lists[q][at] = (check + p) % 2000 + 1;
            check = (check * 31 + difference_of_sum(lists[q], n) + p) % 1000000007;
        }
    }
    printf("%lld passes over 50 lists of 2000: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
