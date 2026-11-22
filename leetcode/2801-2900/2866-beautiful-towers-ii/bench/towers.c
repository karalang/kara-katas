// LeetCode #2866: Beautiful Towers II -- the bench, as towers.kara: 50
// arrays of 10^5 towers, each answered 10 times by the stack arm. The
// stack and both sides are allocated on each call, as the other
// languages' vectors are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t maximum_sum_of_heights(const int64_t *h, int64_t n) {
    int64_t *left = malloc(n * sizeof *left), *right = malloc(n * sizeof *right);
    int64_t *stack = malloc(n * sizeof *stack), top = 0, best = 0;
    for (int64_t i = 0; i < n; i++) {
        while (top > 0 && h[stack[top - 1]] > h[i]) top--;
        left[i] = top > 0 ? left[stack[top - 1]] + (i - stack[top - 1]) * h[i] : (i + 1) * h[i];
        stack[top++] = i;
    }
    top = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        while (top > 0 && h[stack[top - 1]] > h[i]) top--;
        right[i] = top > 0 ? right[stack[top - 1]] + (stack[top - 1] - i) * h[i] : (n - i) * h[i];
        stack[top++] = i;
        int64_t here = left[i] + right[i] - h[i];
        if (here > best) best = here;
    }
    free(left);
    free(right);
    free(stack);
    return best;
}

static int64_t seed = 2866;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 50, rounds = 10, n = 100000;
    int64_t *arrays = malloc(count * n * sizeof *arrays);
    for (int64_t c = 0; c < count; c++) {
        int64_t top = c % 2 == 0 ? 1000000000 : 50;
        for (int64_t i = 0; i < n; i++) arrays[c * n + i] = wide() % top + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t best = maximum_sum_of_heights(arrays + c * n, n);
            total += best;
            check = (check * 31 + best % 1000000007 + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: sums total %lld, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}
