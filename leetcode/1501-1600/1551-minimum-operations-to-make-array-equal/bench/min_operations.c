// LeetCode #1551: Minimum Operations to Make Array Equal -- bench: the ★
// arm (the lower half's distance from the mean, added up place by place)
// for every n from 1 to 10000, in 100 passes. C mirror of min_operations.kara.

#include <stdint.h>
#include <stdio.h>

static int64_t min_operations(int64_t n) {
    int64_t operations = 0;
    for (int64_t i = 0; i < n / 2; i++) operations += n - (2 * i + 1);
    return operations;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100; pass++)
        for (int64_t n = 1; n <= 10000; n++) check = mix(check, min_operations(n) + pass);
    printf("100 passes over n from 1 to 10000: checksum %lld\n", (long long)check);
    return 0;
}
