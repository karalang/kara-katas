// LeetCode #1300 bench: the ★ arm (the numbers sorted and walked from the
// smallest; the best cap is the target's share of what is left, rounded down
// or up) over 50 arrays of 10^4 numbers, up to 20, 100, 1000, 10^4 or 10^5 in
// turn, built once; then 200 passes, each setting one number of every array
// and its target from the checksum so far, answering it, and folding the
// answer into the checksum. The copy is sorted with qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t abs64(int64_t x) { return x < 0 ? -x : x; }

static int64_t find_best_value(const int64_t *arr, int64_t n, int64_t target) {
    int64_t *sorted = malloc(sizeof(int64_t) * n);
    memcpy(sorted, arr, sizeof(int64_t) * n);
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t before = 0, answer = sorted[n - 1];
    for (int64_t i = 0; i < n; i++) {
        int64_t left = n - i;
        if (before + sorted[i] * left >= target) {
            int64_t x = (target - before) / left;
            int64_t low = abs64(before + x * left - target);
            int64_t high = abs64(before + (x + 1) * left - target);
            answer = low <= high ? x : x + 1;
            break;
        }
        before += sorted[i];
    }
    free(sorted);
    return answer;
}

static int64_t seed = 1300;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t tops[5] = {20, 100, 1000, 10000, 100000};
    int64_t *arrays[50];
    for (int t = 0; t < 50; t++) {
        arrays[t] = malloc(sizeof(int64_t) * 10000);
        for (int j = 0; j < 10000; j++) {
            int64_t hi = next_random();
            arrays[t][j] = 1 + (hi * 32768 + next_random()) % tops[t % 5];
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 200; p++) {
        for (int t = 0; t < 50; t++) {
            arrays[t][check % 10000] = 1 + check % tops[t % 5];
            int64_t target = 1 + (check * 7919) % 100000;
            check = (check * 31 + find_best_value(arrays[t], 10000, target) + p) % 1000000007;
        }
    }
    printf("200 passes over 50 arrays of 10^4: checksum %lld\n", (long long)check);
    for (int t = 0; t < 50; t++) free(arrays[t]);
    return 0;
}
