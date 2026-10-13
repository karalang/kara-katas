// Benchmark for #476: C mirror of the ★ arm (a mask of the number's own
// width); see number_complement.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t find_complement(int64_t num) {
    int64_t mask = 1;
    while (mask < num) {
        mask = (mask << 1) | 1;
    }
    return num ^ mask;
}

static int64_t seed = 476;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int count = 30000000;
    int64_t total = 0;
    int64_t checksum = 0;
    for (int i = 0; i < count; i++) {
        int64_t bits = 1 + next_random() % 31;
        int64_t high = (int64_t)1 << (bits - 1);
        int64_t a = next_random();
        int64_t b = next_random();
        int64_t num = high | ((a * 32768 + b) % high);
        int64_t got = find_complement(num);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    printf("%d numbers: complements add up to %lld, checksum %lld\n", count, (long long)total, (long long)checksum);
    return 0;
}
