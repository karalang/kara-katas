// Benchmark for #509: C mirror of the ★ arm (two running values); see
// fib.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t fib(int64_t n) {
    int64_t a = 0, b = 1;
    for (int64_t i = 0; i < n; i++) {
        int64_t next = a + b;
        a = b;
        b = next;
    }
    return a;
}

int main(void) {
    // F(n) for n = 0, 1, ..., 30 over and over, 150,000,000 calls, the
    // results added up modulo 10^9 + 7.
    int64_t calls = 150000000;
    int64_t total = 0;
    for (int64_t i = 0; i < calls; i++) total = (total + fib(i % 31)) % 1000000007;
    printf("%lld calls: total %lld\n", (long long)calls, (long long)total);
    return 0;
}
