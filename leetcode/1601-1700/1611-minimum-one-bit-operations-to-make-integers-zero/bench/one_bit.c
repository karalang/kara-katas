// LeetCode #1611: Minimum One Bit Operations to Make Integers Zero -- the
// bench in C, mirroring one_bit.kara: n turned back from Gray code, the
// XOR of n and all its right shifts.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 10000000

static int32_t minimum_one_bit_operations(int32_t n) {
    int32_t k = 0;
    while (n > 0) {
        k ^= n;
        n >>= 1;
    }
    return k;
}

static int64_t seed = 1611;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *numbers = malloc(sizeof(int32_t) * COUNT);
    for (int i = 0; i < COUNT; i++) {
        int64_t a = next_random();
        int64_t b = next_random();
        numbers[i] = (int32_t)((a * 32768 + b) % 1000000001);
    }
    int64_t check = 0, total = 0;
    for (int i = 0; i < COUNT; i++) {
        int32_t ops = minimum_one_bit_operations(numbers[i]);
        check = (check * 31 + ops + 1) % 1000000007;
        total += ops;
    }
    printf("10000000 numbers up to 10^9: total %lld, checksum %lld\n", (long long)total, (long long)check);
    free(numbers);
    return 0;
}
