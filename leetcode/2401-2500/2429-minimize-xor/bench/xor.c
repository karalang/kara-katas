// LeetCode #2429: Minimize XOR -- the bench, the ★ arm: num1's set bits
// taken from the top while bits are left to place, the rest laid in its
// clear bits from the bottom.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimize_xor(int64_t num1, int64_t num2) {
    int64_t left = __builtin_popcountll((unsigned long long)num2);
    int64_t x = 0;
    for (int bit = 30; bit >= 0; bit--)
        if (left > 0 && ((num1 >> bit) & 1) == 1) {
            x |= (int64_t)1 << bit;
            left--;
        }
    for (int bit = 0; bit < 31; bit++)
        if (left > 0 && ((x >> bit) & 1) == 0) {
            x |= (int64_t)1 << bit;
            left--;
        }
    return x;
}

static int64_t seed = 2429;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int n = 100000;
    int64_t *firsts = malloc(n * sizeof(int64_t));
    int64_t *seconds = malloc(n * sizeof(int64_t));
    for (int i = 0; i < n; i++) {
        int64_t a = next_random();
        firsts[i] = 1 + (a * 32768 + next_random()) % 1000000000;
        int64_t b = next_random();
        seconds[i] = 1 + (b * 32768 + next_random()) % 1000000000;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (int i = 0; i < n; i++)
            check = (check * 31 + minimize_xor(firsts[i], seconds[i] ^ (p + 1)) + p) % 1000000007;
    printf("10 passes over 10^5 pairs: checksum %lld\n", (long long)check);
    free(firsts);
    free(seconds);
    return 0;
}
