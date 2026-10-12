// LeetCode #414: Third Maximum Number -- C mirror of third_max.kara
// (three slots). Usage: ./third_max [rounds]
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t third_max(const int64_t *nums, int64_t n) {
    int has1 = 0, has2 = 0, has3 = 0;
    int64_t first = 0, second = 0, third = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        if ((has1 && x == first) || (has2 && x == second) || (has3 && x == third)) {
            continue;
        }
        if (!has1) {
            first = x;
            has1 = 1;
            continue;
        }
        if (x > first) {
            third = second;
            has3 = has2;
            second = first;
            has2 = 1;
            first = x;
            continue;
        }
        if (!has2) {
            second = x;
            has2 = 1;
            continue;
        }
        if (x > second) {
            third = second;
            has3 = 1;
            second = x;
            continue;
        }
        if (!has3 || x > third) {
            third = x;
            has3 = 1;
        }
    }
    return has3 ? third : first;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t value(int64_t *seed) {
    int64_t high = step(seed);
    int64_t low = step(seed);
    return high * 131072 + low * 4 - 2147483648LL;
}

int main(int argc, char **argv) {
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 50000;
    int64_t n = 10000, seed = 414;
    int64_t *nums = malloc(n * sizeof *nums);
    for (int64_t i = 0; i < n; i++) {
        nums[i] = value(&seed);
    }
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        nums[r * 7919 % n] = value(&seed);
        int64_t answer = third_max(nums, n);
        total += answer;
        checksum = (checksum * 31 + answer % 1000000007 + 1000000007) % 1000000007;
    }
    printf("%lld rounds on %lld numbers: total %lld, checksum %lld\n", (long long)rounds, (long long)n, (long long)total, (long long)checksum);
    free(nums);
    return 0;
}
