// LeetCode #2029: Stone Game IX -- the ★ arm in C, the same algorithm and
// workload as stones.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool stone_game_ix(const int64_t *stones, int64_t n) {
    int64_t cnt[3] = {0, 0, 0};
    for (int64_t i = 0; i < n; i++) cnt[stones[i] % 3] += 1;
    if (cnt[0] % 2 == 0) return cnt[1] >= 1 && cnt[2] >= 1;
    return llabs(cnt[1] - cnt[2]) > 2;
}

static int64_t seed = 2029;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t games[20][100000];
    for (int64_t a = 0; a < 20; a++) {
        for (int i = 0; i < 100000; i++) {
            int64_t base = 3 * (next_random() % 3333);
            int64_t residue;
            if (next_random() % 10 < a % 5) residue = 3;
            else if (next_random() % 10 < 3 * a % 11) residue = 1;
            else residue = 2;
            games[a][i] = base + residue;
        }
    }
    int64_t calls = 0, wins = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        for (int64_t a = 0; a < 20; a++) {
            games[a][(round * 997 + a * 31) % 100000] += 1;
            bool answer = stone_game_ix(games[a], 100000);
            calls++;
            if (answer) wins++;
            check = (check * 31 + (answer ? 1 : 2)) % 1000000007;
        }
    }
    printf("%lld calls: Alice wins %lld, checksum %lld\n", (long long)calls, (long long)wins, (long long)check);
    return 0;
}
