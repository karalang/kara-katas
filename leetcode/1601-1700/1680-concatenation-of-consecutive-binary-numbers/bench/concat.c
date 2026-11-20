// LeetCode #1680: Concatenation of Consecutive Binary Numbers -- the bench's
// C mirror: the ★ arm on 800 random n up to 100000, all drawn first, each
// answered 5 times.

#include <stdint.h>
#include <stdio.h>

#define COUNT 800
#define ROUNDS 5

static int32_t concatenated_binary(int32_t n) {
    const int64_t modulus = 1000000007;
    int64_t value = 0;
    int bits = 0;
    for (int64_t i = 1; i <= n; i++) {
        if ((i & (i - 1)) == 0) bits += 1;
        value = ((value << bits) + i) % modulus;
    }
    return (int32_t)value;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1680;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t ns[COUNT];
    for (int c = 0; c < COUNT; c++) ns[c] = (int32_t)((next_random() * 32768 + next_random()) % 100000 + 1);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = concatenated_binary(ns[c]);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d values of n, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, ROUNDS, (long long)total, (long long)check);
    return 0;
}
