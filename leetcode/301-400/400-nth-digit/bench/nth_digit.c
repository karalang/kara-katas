// Benchmark for #400: mirror of nth_digit.kara (skip whole blocks).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_nth_digit(int64_t n) {
    int64_t rest = n, digits = 1, count = 9, start = 1;
    while (rest > digits * count) {
        rest -= digits * count;
        digits += 1;
        count *= 10;
        start *= 10;
    }
    int64_t number = start + (rest - 1) / digits;
    int64_t shift = digits - 1 - (rest - 1) % digits;
    int64_t x = number;
    while (shift > 0) {
        x = x / 10;
        shift -= 1;
    }
    return x % 10;
}

static int64_t seed = 4001;

static int64_t step(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(int argc, char **argv) {
    int64_t calls = argc > 1 ? atoll(argv[1]) : 10000000;
    int64_t total = 0, checksum = 0;
    for (int64_t c = 0; c < calls; c++) {
        int64_t hi = step();
        int64_t n = 1 + (hi * 32768 + step()) % 2147483647;
        int64_t d = find_nth_digit(n);
        total += d;
        checksum = (checksum * 31 + d) % 1000000007;
    }
    printf("%lld calls: total %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)checksum);
    return 0;
}
