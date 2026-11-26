// LeetCode #1406 bench, C: the same lead from the last stone back,
// workload and checksum as stone_game_iii.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define POOL 100000
#define ROW 50000

// 1 for Alice, 2 for Bob, 3 for a tie
static int stone_game_iii(const int32_t *stone_value, int n, int32_t *best) {
    best[n] = 0;
    for (int i = n - 1; i >= 0; i--) {
        int32_t taken = 0;
        best[i] = INT32_MIN;
        for (int k = 1; k <= 3; k++) {
            if (i + k > n) {
                break;
            }
            taken += stone_value[i + k - 1];
            int32_t lead = taken - best[i + k];
            if (lead > best[i]) {
                best[i] = lead;
            }
        }
    }
    return best[0] > 0 ? 1 : best[0] < 0 ? 2 : 3;
}

int main(void) {
    static int32_t pool[POOL], row[ROW], best[ROW + 1];
    int64_t seed = 1406;
    for (int i = 0; i < POOL; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        pool[i] = (int32_t)(seed / 65536 % 41 - 20);
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 1000; r++) {
        int64_t at = (check + r * 7919) % 50001;
        memcpy(row, pool + at, sizeof(int32_t) * ROW);
        check = (check * 131 + stone_game_iii(row, ROW, best)) % 1000000007;
    }
    printf("1000 rows of 5 * 10^4 stones: checksum %lld\n", (long long)check);
    return 0;
}
