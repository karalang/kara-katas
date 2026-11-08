// LeetCode #1063: Number of Valid Subarrays -- the benchmark, the same
// left-to-right stack as num_valid.kara, in a growable array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t valid_subarrays(const int64_t *nums, int64_t n) {
    int64_t cap = 4, len = 0;
    int64_t *stack = malloc(cap * sizeof *stack);
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        while (len > 0 && stack[len - 1] > x) len--;
        if (len == cap) {
            cap *= 2;
            stack = realloc(stack, cap * sizeof *stack);
        }
        stack[len++] = x;
        count += len;
    }
    free(stack);
    return count;
}

static int64_t seed = 1063;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// `n` numbers drawn from 0 to `k - 1`.
static int64_t *random_array(int64_t n, int64_t k) {
    int64_t *a = malloc(n * sizeof *a);
    for (int64_t i = 0; i < n; i++) a[i] = next_random() % k;
    return a;
}

int main(void) {
    // 20 arrays of 100000 numbers below 2 to 685902, built once, then each
    // answered on 50 of its suffixes
    int64_t *arrays[20];
    for (int64_t a = 0; a < 20; a++) arrays[a] = random_array(100000, 2 + a * a * a * 100);
    int64_t calls = 0, total = 0, check = 0;
    for (int a = 0; a < 20; a++) {
        for (int64_t p = 0; p < 50; p++) {
            int64_t answer = valid_subarrays(arrays[a] + p * 100, 100000 - p * 100);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
            calls++;
        }
    }
    printf("%lld calls: answers sum %lld, checksum %lld\n", (long long)calls, (long long)total,
           (long long)check);
    return 0;
}
