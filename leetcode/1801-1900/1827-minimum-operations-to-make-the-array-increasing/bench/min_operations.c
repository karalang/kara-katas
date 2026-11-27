// LeetCode #1827: Minimum Operations to Make the Array Increasing -- the bench
// in C: the ★ arm over 10000 calls on runs of 2500 to 4999 numbers cut from
// one list of 10^4 numbers from 1 to 10^4, built once, each run's start and
// length drawn from the checksum so far.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t min_operations(const int64_t *nums, int64_t n) {
    int64_t operations = 0, last = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (x <= last) {
            last += 1;
            operations += last - x;
        } else {
            last = x;
        }
    }
    return operations;
}

static int64_t seed = 1827;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *base = malloc(10000 * sizeof(int64_t));
    for (int64_t i = 0; i < 10000; i++) base[i] = 1 + next_random() % 10000;
    int64_t check = 0;
    for (int64_t call = 0; call < 10000; call++) {
        int64_t start = (check + call) % 5000;
        int64_t len = 2500 + (check * 7 + call) % 2500;
        int64_t *run = malloc((size_t)len * sizeof(int64_t));
        memcpy(run, base + start, (size_t)len * sizeof(int64_t));
        check = (check * 31 + min_operations(run, len)) % 1000000007;
        free(run);
    }
    printf("10000 calls: checksum %lld\n", (long long)check);
    free(base);
    return 0;
}
