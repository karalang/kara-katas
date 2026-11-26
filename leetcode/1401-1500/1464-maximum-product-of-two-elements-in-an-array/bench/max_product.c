// LeetCode #1464 bench in C: the ★ arm (one pass keeping the two largest
// values) on the same 1000 arrays of 500 values and 100 passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int max_product(const int *nums, int n) {
    int first = 0, second = 0;
    for (int i = 0; i < n; i++) {
        int x = nums[i];
        if (x > first) {
            second = first;
            first = x;
        } else if (x > second) {
            second = x;
        }
    }
    return (first - 1) * (second - 1);
}

static int64_t seed = 1464;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int *arrays = malloc(sizeof(int) * 1000 * 500);
    for (int p = 0; p < 1000; p++)
        for (int i = 0; i < 500; i++) arrays[p * 500 + i] = (int)(1 + next_random() % 1000);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100; pass++) {
        for (int p = 0; p < 1000; p++) {
            int k = (int)(check % 500);
            arrays[p * 500 + k] = (int)(1 + (check / 7) % 1000);
            int got = max_product(arrays + p * 500, 500);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    printf("100 passes over 1000 arrays of 500 values: checksum %lld\n", (long long)check);
    free(arrays);
    return 0;
}
