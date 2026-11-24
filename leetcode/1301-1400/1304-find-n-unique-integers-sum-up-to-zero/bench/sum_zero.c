// LeetCode #1304 bench in C: the ★ arm (the pairs i and -i, and 0 when n
// is odd, written into a fresh `malloc` of n numbers), the same 10^6
// calls.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *sum_zero(int64_t n) {
    int64_t *out = malloc(sizeof(int64_t) * (size_t)n);
    int64_t len = 0;
    for (int64_t i = 1; i <= n / 2; i++) {
        out[len++] = i;
        out[len++] = -i;
    }
    if (n % 2 == 1) out[len++] = 0;
    return out;
}

int main(void) {
    int64_t check = 0;
    for (int64_t call = 0; call < 1000000; call++) {
        int64_t n = 1 + check % 1000;
        int64_t *got = sum_zero(n);
        int64_t x = got[(check / 1000) % n];
        free(got);
        check = (check * 31 + x + 1000 + call) % 1000000007;
    }
    printf("1000000 calls: checksum %lld\n", (long long)check);
    return 0;
}
