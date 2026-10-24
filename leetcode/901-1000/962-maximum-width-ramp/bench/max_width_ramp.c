// Benchmark: LeetCode #962 Maximum Width Ramp -- the ★ arm, decreasing
// stack, on 50000 numbers, LeetCode's largest, falling overall with
// noise. Each call first sets one number to a new random value. Mirrors
// max_width_ramp.kara, .rs, .py and go-seq/. The stack is a malloc'd
// array per call, as the other languages' growable arrays are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 50000
#define COUNT 50

static int64_t seed = 962;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t max_width_ramp(const int64_t *nums, int64_t n) {
    int64_t *stack = malloc(sizeof(int64_t) * n);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        if (top == 0 || nums[i] < nums[stack[top - 1]]) stack[top++] = i;
    }
    int64_t best = 0;
    for (int64_t j = n - 1; j >= 0 && top > 0; j--) {
        while (top > 0 && nums[stack[top - 1]] <= nums[j]) {
            int64_t w = j - stack[top - 1];
            if (w > best) best = w;
            top--;
        }
    }
    free(stack);
    return best;
}

static int64_t cases[COUNT][N];

int main(void) {
    int rounds = 40;
    for (int i = 0; i < COUNT; i++) {
        int64_t step = 1 + i % 5, noise = 10 * (i / 5);
        for (int64_t p = 0; p < N; p++) cases[i][p] = 50000 - noise - p / step + next_random() % (noise + 1);
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < COUNT; i++) {
            int c = (r + i) % COUNT;
            int64_t p = next_random() % N;
            cases[c][p] = next_random() % 50001;
            int64_t w = max_width_ramp(cases[c], N);
            total += w;
            check = (check * 31 + w + i) % 1000000007;
        }
    }
    printf("%d rounds over 50 cases of 50000 numbers: the ramps sum to %lld, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
