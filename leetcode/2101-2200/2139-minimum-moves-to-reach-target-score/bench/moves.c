// LeetCode #2139: Minimum Moves to Reach Target Score -- the benchmark,
// the same algorithm as moves.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t min_moves(int64_t target, int64_t max_doubles) {
    int64_t doubles = max_doubles, moves = 0;
    while (target > 1 && doubles > 0) {
        if (target % 2 == 1) {
            target -= 1;
        } else {
            target /= 2;
            doubles -= 1;
        }
        moves += 1;
    }
    return moves + target - 1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2139;
    int64_t targets[1000];
    for (int i = 0; i < 1000; i++) {
        int64_t hi = next_random(&seed);
        targets[i] = (hi * 32768 + next_random(&seed)) % 1000000000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < 4000; r++) {
        for (int i = 0; i < 1000; i++) {
            int64_t moves = min_moves(targets[i] + r, r % 40);
            total += moves;
            check = (check * 31 + moves) % 1000000007;
        }
    }
    printf("4000000 solves: %lld moves in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
