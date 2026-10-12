// Benchmark for #397: mirror of integer_replacement.kara (greedy on the last two bits).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t integer_replacement(int64_t n) {
    int64_t v = n, ops = 0;
    while (v != 1) {
        if (v % 2 == 0) {
            v = v / 2;
        } else if (v == 3 || v % 4 == 1) {
            v -= 1;
        } else {
            v += 1;
        }
        ops += 1;
    }
    return ops;
}

static int64_t seed = 397;

static int64_t step(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(int argc, char **argv) {
    int64_t calls = argc > 1 ? atoll(argv[1]) : 5000000;
    int64_t total = 0, checksum = 0;
    for (int64_t c = 0; c < calls; c++) {
        int64_t hi = step();
        int64_t n = 1 + (hi * 32768 + step()) % 2147483647;
        int64_t r = integer_replacement(n);
        total += r;
        checksum = (checksum * 31 + r) % 1000000007;
    }
    printf("%lld calls: total %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)checksum);
    return 0;
}
