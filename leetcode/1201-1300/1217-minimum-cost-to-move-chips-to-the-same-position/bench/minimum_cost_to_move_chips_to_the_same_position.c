// LeetCode #1217 bench, in C: the ★ arm (the odd and the even chips
// counted, the lesser count the cost) on 20000 sets of 100 chips at
// positions up to 10^9, drawn once; then 20 rounds over the sets, every
// answer folded into a checksum.

#include <stdio.h>
#include <stdlib.h>

#define SETS 20000
#define CHIPS 100

static long long seed = 1217;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long min_cost_to_move_chips(const long long *position, int n) {
    long long odd = 0, even = 0;
    for (int i = 0; i < n; i++) {
        if (position[i] % 2 == 1) odd++;
        else even++;
    }
    return odd < even ? odd : even;
}

int main(void) {
    long long *sets = malloc(sizeof(long long) * SETS * CHIPS);
    for (int s = 0; s < SETS; s++)
        for (int i = 0; i < CHIPS; i++) {
            long long hi = next_random();
            long long lo = next_random();
            sets[s * CHIPS + i] = (hi * 32768 + lo) % 1000000000LL + 1;
        }
    long long check = 0;
    for (long long round = 0; round < 20; round++)
        for (int s = 0; s < SETS; s++)
            check = (check * 131 + min_cost_to_move_chips(sets + s * CHIPS, CHIPS) + round) % 1000000007LL;
    printf("20 rounds over 20000 sets of 100 chips: checksum %lld\n", check);
    free(sets);
    return 0;
}
