// LeetCode #704 bench: the ★ arm in C. See the .kara twin for the
// workload.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t search(const int64_t *nums, int64_t n, int64_t target) {
    int64_t lo = 0;
    int64_t hi = n - 1;
    while (lo <= hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) {
            return mid;
        }
        if (nums[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 704;
    int64_t *arrays[100];
    for (int a = 0; a < 100; a++) {
        int64_t *nums = malloc(sizeof(int64_t) * 10000);
        int64_t v = -9999;
        for (int i = 0; i < 10000; i++) {
            nums[i] = v;
            v += 1 + next_random(&seed) % 2;
        }
        arrays[a] = nums;
    }
    int64_t found = 0;
    int64_t checksum = 0;
    for (int round = 0; round < 5; round++) {
        for (int a = 0; a < 100; a++) {
            for (int64_t target = -9999; target < 10000; target++) {
                int64_t at = search(arrays[a], 10000, target);
                if (at >= 0) {
                    found += 1;
                }
                checksum = (checksum * 31 + at + 1) % 1000000007;
            }
        }
    }
    printf("5 rounds of 100 arrays of 10000: %lld found, checksum %lld\n",
           (long long)found, (long long)checksum);
    for (int a = 0; a < 100; a++) {
        free(arrays[a]);
    }
    return 0;
}
