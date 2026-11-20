// LeetCode #2289: Steps to Make Array Non-decreasing -- the bench, the ★
// arm in C. A stack of the elements still standing to the left, each with
// the step at which it is removed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { ARRAYS = 50, N = 10000 };

static int64_t total_steps(const int64_t *nums, int n, int64_t *values, int64_t *steps) {
    int top = 0;
    int64_t most = 0;
    for (int i = 0; i < n; i++) {
        int64_t x = nums[i];
        int64_t step = 0;
        while (top > 0 && values[top - 1] <= x) {
            if (steps[top - 1] > step) step = steps[top - 1];
            top--;
        }
        step = top == 0 ? 0 : step + 1;
        if (step > most) most = step;
        values[top] = x;
        steps[top] = step;
        top++;
    }
    return most;
}

static int64_t seed = 2289;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[ARRAYS][N];
    for (int a = 0; a < ARRAYS; a++)
        for (int i = 0; i < N; i++) arrays[a][i] = (int64_t)i * 3 + next_random() % 20000;
    int64_t *values = malloc(sizeof(int64_t) * N);
    int64_t *steps = malloc(sizeof(int64_t) * N);
    int64_t check = 0;
    for (int p = 0; p < 20; p++) {
        int64_t total = 0;
        for (int a = 0; a < ARRAYS; a++) total += total_steps(arrays[a], N, values, steps);
        check = (check * 31 + total) % 1000000007;
    }
    printf("20 passes over 50 arrays of 10^4: checksum %lld\n", (long long)check);
    free(values);
    free(steps);
    return 0;
}
