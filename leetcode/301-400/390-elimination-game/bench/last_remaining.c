// Benchmark for #390: mirror of last_remaining.kara (follow the head).
#include <stdint.h>
#include <stdio.h>

static int64_t last_remaining(int64_t n) {
    int64_t head = 1, step = 1, left = n;
    int from_left = 1;
    while (left > 1) {
        if (from_left || left % 2 == 1) {
            head += step;
        }
        left /= 2;
        step *= 2;
        from_left = !from_left;
    }
    return head;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 390, total = 0, checksum = 0;
    for (int i = 0; i < 10000000; i++) {
        int64_t hi = next(&seed);
        int64_t n = hi * 32768 + next(&seed) + 1;
        int64_t r = last_remaining(n);
        total += r;
        checksum = (checksum * 31 + r) % 1000000007;
    }
    printf("10000000 values of n, sum %lld, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
