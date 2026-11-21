// LeetCode #2439: Minimize Maximum of Array -- the bench, the ★ arm: the
// largest ceiling average of any prefix, in one pass.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimize_array_value(const int64_t *nums, int64_t n) {
    int64_t sum = 0, answer = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        int64_t a = (sum + i) / (i + 1);
        if (a > answer) answer = a;
    }
    return answer;
}

static int64_t seed = 2439;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return (a * 32768 + next_random()) % 1000000001;
}

int main(void) {
    int64_t *arrays[10];
    for (int c = 0; c < 10; c++) {
        arrays[c] = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) arrays[c][i] = wide();
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++)
        for (int64_t c = 0; c < 10; c++) {
            int64_t at = (p * 7919 + c * 104729) % 100000;
            arrays[c][at] = wide();
            check = (check * 31 + minimize_array_value(arrays[c], 100000) + p) % 1000000007;
        }
    printf("100 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int c = 0; c < 10; c++) free(arrays[c]);
    return 0;
}
