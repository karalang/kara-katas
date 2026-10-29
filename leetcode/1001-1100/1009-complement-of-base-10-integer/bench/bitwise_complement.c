// LeetCode #1009 bench: the ★ arm (an all-ones mask) over 1,000,000 n
// below 10^9, of random lengths, drawn once; each of 50 rounds takes the
// complement of every n plus the round number and folds the round's sum
// into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t bitwise_complement(int64_t n) {
    int64_t mask = 1;
    while (mask < n) mask = mask * 2 + 1;
    return mask ^ n;
}

static int64_t seed = 1009;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 1000000, ROUNDS = 50 };
    int64_t *values = malloc(COUNT * sizeof(int64_t));
    for (int k = 0; k < COUNT; k++) {
        int64_t bits = 1 + next_random() % 30;
        int64_t hi = next_random();
        int64_t lo = next_random();
        values[k] = ((hi * 32768 + lo) % (1LL << bits)) % 999999000;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t sum = 0;
        for (int64_t k = 0; k < COUNT; k++) sum += bitwise_complement(values[k] + r);
        check = (check * 31 + sum) % 1000000007;
    }
    printf("%d rounds over %d values of n: checksum %lld\n", ROUNDS, COUNT, (long long)check);
    free(values);
    return 0;
}
