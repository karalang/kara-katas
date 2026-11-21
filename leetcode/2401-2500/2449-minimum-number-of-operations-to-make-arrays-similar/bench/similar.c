// LeetCode #2449: Minimum Number of Operations to Make Arrays Similar --
// the bench, the ★ arm: the odd and the even values of each array sorted
// and matched in order, the distance over 4.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return x < y ? -1 : x > y;
}

// the odd values of `values` into `odd` and the even into `even`, each
// sorted; returns how many are odd
static int64_t split_sorted(const int64_t *values, int64_t n, int64_t *odd, int64_t *even) {
    int64_t o = 0, e = 0;
    for (int64_t i = 0; i < n; i++) {
        if (values[i] % 2 == 1) odd[o++] = values[i];
        else even[e++] = values[i];
    }
    qsort(odd, o, sizeof(int64_t), by_value);
    qsort(even, e, sizeof(int64_t), by_value);
    return o;
}

static int64_t make_similar(const int64_t *nums, const int64_t *target, int64_t n) {
    int64_t *odd = malloc(n * sizeof(int64_t)), *even = malloc(n * sizeof(int64_t));
    int64_t *odd_target = malloc(n * sizeof(int64_t)), *even_target = malloc(n * sizeof(int64_t));
    int64_t o = split_sorted(nums, n, odd, even);
    split_sorted(target, n, odd_target, even_target);
    int64_t distance = 0;
    for (int64_t i = 0; i < o; i++) distance += llabs(odd[i] - odd_target[i]);
    for (int64_t i = 0; i < n - o; i++) distance += llabs(even[i] - even_target[i]);
    free(odd);
    free(even);
    free(odd_target);
    free(even_target);
    return distance / 4;
}

static int64_t seed = 2449;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}
static int64_t wide_random(void) {
    int64_t r = next_random();
    return r * 32768 + next_random();
}

int main(void) {
    const int64_t n = 100000;
    int64_t *nums = malloc(n * sizeof(int64_t)), *target = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) nums[i] = 1 + wide_random() % 1000000;
    for (int64_t i = 0; i < n; i++) target[i] = nums[i];
    int64_t check = 0;
    for (int64_t p = 0; p < 220; p++) {
        for (int t = 0; t < 1000; t++) {
            int64_t i = wide_random() % n;
            int64_t j = wide_random() % n;
            int64_t step = 2 * (1 + next_random() % 50);
            if (i != j && target[i] + step <= 1000000 && target[j] - step >= 1) {
                target[i] += step;
                target[j] -= step;
            }
        }
        check = (check * 31 + make_similar(nums, target, n) + p) % 1000000007;
    }
    printf("220 passes over 10^5 values: checksum %lld\n", (long long)check);
    free(nums);
    free(target);
    return 0;
}
