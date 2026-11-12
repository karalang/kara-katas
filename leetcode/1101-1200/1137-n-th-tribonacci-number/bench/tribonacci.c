// LeetCode #1137: N-th Tribonacci Number -- the bench, the ★ arm's algorithm:
// three running values.
#include <stdint.h>
#include <stdio.h>

static int64_t tribonacci(int64_t n) {
    int64_t a = 0, b = 1, c = 1;
    for (int64_t i = 0; i < n; i++) {
        int64_t next = a + b + c;
        a = b;
        b = c;
        c = next;
    }
    return a;
}

static int64_t seed = 1137;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int64_t q = 0; q < 20000000; q++) {
        int64_t n = next_random() % 38;
        int64_t t = tribonacci(n);
        total += t;
        check = (check * 31 + t % 1000003) % 1000000007;
    }
    printf("20000000 queries, n from 0 to 37: answers total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
