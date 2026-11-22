// LeetCode #2712: Minimum Cost to Make All Characters Equal -- the bench
// (equal.kara in C): each boundary between unequal neighbours priced at
// the cheaper flip across it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimum_cost(const char *bits, int64_t n) {
    int64_t cost = 0;
    for (int64_t i = 1; i < n; i++) {
        if (bits[i] != bits[i - 1]) cost += i < n - i ? i : n - i;
    }
    return cost;
}

static int64_t seed = 2712;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 100, rounds = 5, n = 100000;
    char *strings = malloc((size_t)count * n);
    for (int c = 0; c < count; c++) {
        int64_t change = next_random() % 9;
        char last = '0';
        for (int i = 0; i < n; i++) {
            if (next_random() % 8 < change) last = last == '0' ? '1' : '0';
            strings[(size_t)c * n + i] = last;
        }
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            int64_t cost = minimum_cost(strings + (size_t)c * n, n);
            sum += cost;
            check = (check * 31 + cost + r) % 1000000007;
        }
    }
    printf("%d strings of 100000 bits, %d rounds: costs sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(strings);
    return 0;
}
