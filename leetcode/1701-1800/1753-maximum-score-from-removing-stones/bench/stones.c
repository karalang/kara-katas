// LeetCode #1753: Maximum Score From Removing Stones -- the bench
// (stones.kara in C): a closed form.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { COUNT = 2000000, ROUNDS = 5 };

static int32_t max32(int32_t a, int32_t b) { return a > b ? a : b; }
static int32_t min32(int32_t a, int32_t b) { return a < b ? a : b; }

static int32_t maximum_score(int32_t a, int32_t b, int32_t c) {
    int32_t total = a + b + c;
    int32_t largest = max32(a, max32(b, c));
    return min32(total / 2, total - largest);
}

static int64_t seed = 1753;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int32_t (*piles)[3] = malloc(sizeof(int32_t[3]) * COUNT);
    for (int64_t i = 0; i < COUNT; i++)
        for (int j = 0; j < 3; j++) piles[i][j] = (int32_t)(wide() % 100000 + 1);
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t answer = maximum_score(piles[i][0], piles[i][1], piles[i][2]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d sets of piles, %d rounds: scores add to %lld, checksum %lld\n", COUNT, ROUNDS, (long long)sum, (long long)check);
    free(piles);
    return 0;
}
