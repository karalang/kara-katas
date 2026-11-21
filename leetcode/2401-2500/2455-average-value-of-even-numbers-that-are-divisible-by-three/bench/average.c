// LeetCode #2455: Average Value of Even Numbers That Are Divisible by
// Three -- bench, C mirror of average.kara: one pass sums and counts the
// values divisible by 6.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t average_value(const int64_t *nums, int64_t n) {
    int64_t sum = 0, count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] % 6 == 0) {
            sum += nums[i];
            count += 1;
        }
    }
    return count == 0 ? 0 : sum / count;
}

static int64_t seed = 2455;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *arrays[1000];
    for (int a = 0; a < 1000; a++) {
        arrays[a] = malloc(sizeof(int64_t) * 1000);
        for (int i = 0; i < 1000; i++) {
            arrays[a][i] = 1 + next_random() % 1000;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 250; p++) {
        for (int64_t a = 0; a < 1000; a++) {
            arrays[a][(p * 7919 + a) % 1000] = 1 + check % 1000;
            check = (check * 31 + average_value(arrays[a], 1000) + p) % 1000000007;
        }
    }
    printf("250 passes over 1000 arrays of 1000 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 1000; a++) free(arrays[a]);
    return 0;
}
