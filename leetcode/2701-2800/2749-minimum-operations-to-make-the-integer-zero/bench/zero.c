// LeetCode #2749: Minimum Operations to Make the Integer Zero -- the
// bench (zero.kara in C): the least k with t = num1 - k num2 a sum of k
// powers of two, by `__builtin_popcountll`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t make_the_integer_zero(int64_t num1, int64_t num2) {
    for (int64_t k = 1; k <= 60; k++) {
        int64_t t = num1 - k * num2;
        if (__builtin_popcountll((uint64_t)t) <= k && k <= t) return k;
    }
    return -1;
}

static int64_t seed = 2749;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 1000000, rounds = 10;
    int64_t (*pairs)[2] = malloc(sizeof(int64_t) * 2 * count);
    for (int i = 0; i < count; i++) {
        int64_t hi = next_random();
        int64_t num1 = (hi * 32768 + next_random()) % 1000000000 + 1;
        hi = next_random();
        int64_t size = (hi * 32768 + next_random()) % 1000000001;
        int64_t num2 = next_random() % 2 == 0 ? size : -size;
        pairs[i][0] = num1;
        pairs[i][1] = num2;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int i = 0; i < count; i++) {
            int64_t steps = make_the_integer_zero(pairs[i][0], pairs[i][1]);
            sum += steps;
            check = (check * 31 + steps + 1 + r) % 1000000007;
        }
    printf("%d pairs, %d rounds: steps sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(pairs);
    return 0;
}
