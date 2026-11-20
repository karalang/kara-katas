// LeetCode #2342: Max Sum of a Pair With Equal Sum of Digits -- the bench,
// the ★ arm in C: a table of 82 keeping the largest value seen for each
// digit sum, each value paired with the largest before it of its own sum.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t digit_sum(int64_t x) {
    int64_t s = 0;
    while (x > 0) {
        s += x % 10;
        x /= 10;
    }
    return s;
}

static int64_t maximum_sum(const int64_t *nums, int64_t n) {
    int64_t *best = malloc(82 * sizeof(int64_t));
    for (int i = 0; i < 82; i++) best[i] = -1;
    int64_t answer = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        int64_t s = digit_sum(x);
        if (best[s] >= 0 && best[s] + x > answer) answer = best[s] + x;
        if (x > best[s]) best[s] = x;
    }
    free(best);
    return answer;
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    int64_t *arrays[10];
    for (int64_t a = 0; a < 10; a++) {
        arrays[a] = malloc(100000 * sizeof(int64_t));
        for (int64_t i = 0; i < 100000; i++) arrays[a][i] = scrambled(a * 100000 + i) % 1000000000 + 1;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++)
        for (int a = 0; a < 10; a++) check = (check * 31 + maximum_sum(arrays[a], 100000) + p) % 1000000007;
    printf("20 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) free(arrays[a]);
    return 0;
}
