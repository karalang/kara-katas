// LeetCode #887 bench: the floors a number of moves can cover, on 30000
// cases of 2 to 9 eggs and up to 10^9 floors. The same algorithm as
// super_egg_drop.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t super_egg_drop(int64_t k, int64_t n) {
    int64_t *floors = calloc((size_t)(k + 1), sizeof(int64_t));
    int64_t moves = 0;
    while (floors[k] < n) {
        moves += 1;
        for (int64_t eggs = k; eggs >= 1; eggs--) {
            floors[eggs] = floors[eggs - 1] + floors[eggs] + 1;
        }
    }
    free(floors);
    return moves;
}

static int64_t seed = 887;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int c = 0; c < 30000; c++) {
        int64_t k = 2 + next_random() % 8;
        int64_t hi = next_random();
        int64_t n = 1 + (hi * 32768 + next_random()) % 1000000000;
        int64_t moves = super_egg_drop(k, n);
        total += moves;
        check = (check * 131 + moves) % 1000000007;
    }
    printf("30000 cases of 2 to 9 eggs and up to 10^9 floors: %lld moves, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
