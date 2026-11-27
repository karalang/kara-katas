// LeetCode #1822: Sign of the Product of an Array -- the bench in C: the ★
// arm over 300000 calls on runs of 500 to 999 numbers cut from one list of
// 2000 numbers from -100 to 100 but zero, built once, each run's start and
// length drawn from the checksum so far. Each call copies its run, as
// `to_vec` does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t array_sign(const int64_t *run, size_t n) {
    int64_t *nums = malloc(n * sizeof *nums);
    memcpy(nums, run, n * sizeof *nums);
    int64_t sign = 1;
    for (size_t i = 0; i < n; i++) {
        if (nums[i] == 0) {
            sign = 0;
            break;
        }
        if (nums[i] < 0) sign = -sign;
    }
    free(nums);
    return sign;
}

static int64_t seed = 1822;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t base[2000];
    for (int i = 0; i < 2000; i++) {
        int64_t x = next_random() % 200 - 100;
        base[i] = x >= 0 ? x + 1 : x;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 300000; call++) {
        size_t start = (size_t)((check + call) % 1000);
        size_t n = (size_t)(500 + (check * 7 + call) % 500);
        check = (check * 3 + array_sign(base + start, n) + 1) % 1000000007;
    }
    printf("300000 calls: checksum %lld\n", (long long)check);
    return 0;
}
