// LeetCode #2855: Minimum Right Shifts to Sort the Array -- the bench:
// the ★ arm over 10^5 arrays of 100 distinct values up to 100,
// LeetCode's most, two times in three sorted and shifted, else with two
// values swapped after it, all drawn first, then each answered 50 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimum_right_shifts(const int64_t *nums, int64_t n) {
    int64_t drop = -1;
    for (int64_t i = 0; i < n - 1; i++) {
        if (nums[i] > nums[i + 1]) {
            if (drop >= 0) return -1;
            drop = i;
        }
    }
    if (drop < 0) return 0;
    if (nums[n - 1] > nums[0]) return -1;
    return n - 1 - drop;
}

static int64_t seed = 2855;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 100000, rounds = 50, n = 100;
    int64_t *arrays = malloc(sizeof(int64_t) * count * n);
    for (int64_t a = 0; a < count; a++) {
        int64_t *nums = arrays + a * n;
        int64_t k = next_random() % 100;
        for (int64_t i = 0; i < n; i++) nums[(i + k) % n] = i + 1;
        if (next_random() % 3 == 2) {
            int64_t i = next_random() % 100;
            int64_t j = next_random() % 100;
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
    }
    int64_t sortable = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t a = 0; a < count; a++) {
            int64_t shifts = minimum_right_shifts(arrays + a * n, n);
            if (shifts >= 0) sortable++;
            check = (check * 31 + shifts + 1 + r) % 1000000007;
        }
    }
    printf("%lld arrays, %lld rounds: %lld sortable, checksum %lld\n", (long long)count, (long long)rounds, (long long)sortable, (long long)check);
    free(arrays);
    return 0;
}
