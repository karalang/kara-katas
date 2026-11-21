// LeetCode #2419: Longest Subarray With Maximum Bitwise AND -- the bench,
// the ★ arm in C: one scan keeping the largest value so far and the run
// of it ending here.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t longest_subarray(const int64_t *nums, int n) {
    int64_t top = 0, run = 0, best = 0;
    for (int k = 0; k < n; k++) {
        int64_t x = nums[k];
        if (x > top) {
            top = x;
            run = 0;
            best = 0;
        }
        if (x == top) {
            run++;
            if (run > best) best = run;
        } else {
            run = 0;
        }
    }
    return best;
}

static int64_t seed = 2419;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[10][N];
    for (int64_t i = 0; i < 10; i++) {
        for (int k = 0; k < N; k++) {
            if (k > 0 && next_random() % 2 == 0) {
                arrays[i][k] = arrays[i][k - 1];
            } else {
                arrays[i][k] = 1 + next_random() % (2 + 100 * i);
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int i = 0; i < 10; i++) {
            check = (check * 31 + longest_subarray(arrays[i], N) + p) % 1000000007;
        }
    }
    printf("500 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    return 0;
}
