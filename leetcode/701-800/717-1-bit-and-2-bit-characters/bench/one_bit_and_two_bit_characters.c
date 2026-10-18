// LeetCode #717: 1-bit and 2-bit Characters -- read from the start.
// Benchmark mirror of the Kara star arm: step past one bit on a 0 and
// two on a 1; the last character is one bit when a step lands on the
// last bit.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int is_one_bit_character(const int64_t *bits, int64_t n) {
    int64_t i = 0;
    while (i < n - 1) i += bits[i] + 1;
    return i == n - 1;
}

enum { STRINGS = 100, N = 10000 };

int main(void) {
    int64_t seed = 717;
    int64_t *strings[STRINGS];
    for (int s = 0; s < STRINGS; s++) {
        int64_t density = 1 + s % 3;
        strings[s] = malloc(N * sizeof(int64_t));
        for (int i = 0; i < N - 1; i++) strings[s][i] = next_random(&seed) % 4 < density ? 1 : 0;
        strings[s][N - 1] = 0;
    }
    int64_t yes = 0;
    for (int64_t round = 0; round < 400; round++) {
        for (int s = 0; s < STRINGS; s++) {
            int64_t at = (round * 997) % 9999;
            strings[s][at] = 1 - strings[s][at];
        }
        for (int s = 0; s < STRINGS; s++)
            if (is_one_bit_character(strings[s], N)) yes++;
    }
    for (int s = 0; s < STRINGS; s++) free(strings[s]);
    printf("400 rounds of 100 strings of 10000 bits: %lld one-bit endings\n", (long long)yes);
    return 0;
}
