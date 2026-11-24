// LeetCode #1318 bench, C mirror of the Kāra bench: the ★ arm (each of the
// 30 bits looked at alone and costed) on 1000 triples of numbers from 1 to
// 10^9 built once; then 3000 passes, each setting one number of every
// triple from the checksum so far, and folding every answer plus the pass
// into the checksum.
#include <stdint.h>
#include <stdio.h>

static int64_t min_flips(int64_t a, int64_t b, int64_t c) {
    int64_t flips = 0;
    for (int64_t i = 0; i < 30; i++) {
        int64_t x = (a >> i) & 1;
        int64_t y = (b >> i) & 1;
        int64_t z = (c >> i) & 1;
        flips += z == 1 ? 1 - (x | y) : x + y;
    }
    return flips;
}

static int64_t seed = 1318;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t big = 1000000000;
    static int64_t nums[3000];
    for (int i = 0; i < 3000; i++) {
        int64_t hi = next_random();
        nums[i] = 1 + (hi * 32768 + next_random()) % big;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 3000; pass++) {
        for (int64_t t = 0; t < 1000; t++) {
            nums[3 * t + check % 3] = 1 + (check * 7919) % big;
            int64_t got = min_flips(nums[3 * t], nums[3 * t + 1], nums[3 * t + 2]);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    printf("3000 passes over 1000 triples: checksum %lld\n", (long long)check);
    return 0;
}
