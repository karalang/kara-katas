// LeetCode #1819: Number of Different Subsequences GCDs -- the bench in C:
// the ★ arm over 100 calls on runs of 50000 to 99999 numbers cut from one
// list of 10^5 numbers from 1 to 2 * 10^5, built once, each run's length
// drawn from the checksum so far. Each call copies its run, as `to_vec`
// does.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

static int64_t count_different_subsequence_gcds(const int64_t *run, size_t n) {
    int64_t *nums = malloc(n * sizeof *nums);
    memcpy(nums, run, n * sizeof *nums);
    int64_t top = nums[0];
    for (size_t i = 1; i < n; i++) if (nums[i] > top) top = nums[i];
    bool *present = calloc((size_t)top + 1, sizeof *present);
    for (size_t i = 0; i < n; i++) present[nums[i]] = true;
    int64_t count = 0;
    for (int64_t g = 1; g <= top; g++) {
        int64_t d = 0;
        for (int64_t m = g; m <= top && d != g; m += g)
            if (present[m]) d = gcd(d, m);
        if (d == g) count++;
    }
    free(present);
    free(nums);
    return count;
}

static int64_t seed = 1819;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t base[100000];
    for (int i = 0; i < 100000; i++) {
        int64_t hi = next_random();
        base[i] = 1 + (hi * 32768 + next_random()) % 200000;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 100; call++) {
        size_t n = (size_t)(50000 + (check + call) % 50000);
        check = (check * 31 + count_different_subsequence_gcds(base, n)) % 1000000007;
    }
    printf("100 calls: checksum %lld\n", (long long)check);
    return 0;
}
