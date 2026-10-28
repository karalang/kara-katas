// Benchmark: LeetCode #1006 Clumsy Factorial -- the ★ arm, a stack, on
// every n up to 10000, LeetCode's largest.
// Mirrors clumsy.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t clumsy(int64_t n) {
    int64_t cap = 4, len = 0;
    int64_t *stack = malloc(cap * sizeof(int64_t));
    stack[len++] = n;
    int64_t op = 0;
    for (int64_t x = n - 1; x > 0; x--) {
        int64_t last = len - 1;
        if (op == 0) {
            stack[last] = stack[last] * x;
        } else if (op == 1) {
            stack[last] = stack[last] / x;
        } else {
            if (len == cap) {
                cap *= 2;
                stack = realloc(stack, cap * sizeof(int64_t));
            }
            stack[len++] = op == 2 ? x : -x;
        }
        op = (op + 1) % 4;
    }
    int64_t sum = 0;
    for (int64_t i = 0; i < len; i++) sum += stack[i];
    free(stack);
    return sum;
}

int main(void) {
    int64_t rounds = 4;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 10000; i++) {
            int64_t n = r % 2 == 0 ? i + 1 : 10000 - i;
            int64_t got = clumsy(n);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("%lld rounds over every n up to 10000: answers sum to %lld, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
