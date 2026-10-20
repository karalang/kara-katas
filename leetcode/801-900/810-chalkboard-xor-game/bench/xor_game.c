// LeetCode 810 -- Chalkboard XOR Game: the bench, with the ★ arm's XOR and
// count.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

static int64_t seed = 810;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static bool xor_game(const int64_t *nums, int64_t n) {
    int64_t x = 0;
    for (int64_t i = 0; i < n; i++) {
        x ^= nums[i];
    }
    return x == 0 || n % 2 == 0;
}

// 64 boards of 999 numbers are made once. Each round writes a new number
// into one place of the next board and asks who wins it.
int main(void) {
    static int64_t boards[64][999];
    for (int k = 0; k < 64; k++) {
        for (int i = 0; i < 999; i++) {
            boards[k][i] = next_random();
        }
    }
    int64_t rounds = 10000000;
    int64_t wins = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = r % 64;
        boards[k][r / 64 % 999] = next_random();
        int64_t win = xor_game(boards[k], 999) ? 1 : 0;
        wins += win;
        check = (check * 131 + win + r % 1000) % 1000000007;
    }
    printf("%lld rounds of 999 numbers: %lld won by Alice, checksum %lld\n",
           (long long)rounds, (long long)wins, (long long)check);
    return 0;
}
