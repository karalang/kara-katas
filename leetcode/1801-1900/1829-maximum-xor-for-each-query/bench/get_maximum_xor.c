// LeetCode #1829: Maximum XOR for Each Query -- the bench in C: the ★ arm over
// 200 calls on the first 50000 to 99999 of one sorted list of 10^5 numbers
// below 2^20, built once, each run's length drawn from the checksum so far,
// and maximumBit 20. Each call copies its run, as the arm takes its list by
// value.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// the answers go to answer, n of them
static void get_maximum_xor(const int64_t *nums, int64_t n, int64_t maximum_bit, int64_t *answer) {
    int64_t mask = ((int64_t)1 << maximum_bit) - 1;
    int64_t all = 0;
    for (int64_t i = 0; i < n; i++) all ^= nums[i];
    int64_t at = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        answer[at++] = all ^ mask;
        all ^= nums[i];
    }
}

static int64_t seed = 1829;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int64_t *base = malloc(100000 * sizeof(int64_t));
    for (int64_t i = 0; i < 100000; i++) {
        int64_t hi = next_random();
        base[i] = (hi * 32768 + next_random()) % 1048576;
    }
    qsort(base, 100000, sizeof(int64_t), by_value);
    int64_t check = 0;
    for (int64_t call = 0; call < 200; call++) {
        int64_t n = 50000 + (check + call) % 50000;
        int64_t *run = malloc((size_t)n * sizeof(int64_t)), *answer = malloc((size_t)n * sizeof(int64_t));
        memcpy(run, base, (size_t)n * sizeof(int64_t));
        get_maximum_xor(run, n, 20, answer);
        int64_t total = 0;
        for (int64_t i = 0; i < n; i++) total += answer[i];
        check = (check * 31 + total % 1000000007) % 1000000007;
        free(run);
        free(answer);
    }
    printf("200 calls: checksum %lld\n", (long long)check);
    free(base);
    return 0;
}
