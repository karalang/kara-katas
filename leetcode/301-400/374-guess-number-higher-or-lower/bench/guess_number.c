// Benchmark for #374 -- mirror of guess_number.kara.

#include <stdint.h>
#include <stdio.h>

typedef struct { int64_t pick, calls; } Game;

static int64_t guess(Game *game, int64_t num) {
    game->calls++;
    if (game->pick < num) return -1;
    if (game->pick > num) return 1;
    return 0;
}

static int64_t guess_number(int64_t n, Game *game) {
    int64_t lo = 1, hi = n;
    while (lo <= hi) {
        int64_t mid = lo + (hi - lo) / 2;
        int64_t answer = guess(game, mid);
        if (answer == 0) return mid;
        if (answer < 0) hi = mid - 1;
        else lo = mid + 1;
    }
    return -1;
}

int main(void) {
    int64_t seed = 374, checksum = 0, guesses = 0;
    for (int round = 0; round < 2000000; round++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t n = 1 + (high * 65536 + seed / 32768) % 2147483647;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t high2 = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t pick = 1 + (high2 * 65536 + seed / 32768) % n;
        Game game = {pick, 0};
        int64_t got = guess_number(n, &game);
        guesses += game.calls;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    printf("%lld guesses, checksum %lld\n", (long long)guesses, (long long)checksum);
    return 0;
}
