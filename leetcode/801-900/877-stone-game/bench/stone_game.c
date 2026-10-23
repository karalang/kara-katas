// LeetCode #877 bench: C mirror of stone_game.kara (the ★ arm, the best
// margin of every run of piles) on the same 1,000 games; the table is
// malloc'd row by row for each game.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int stone_game(const int64_t *piles, int n) {
    int64_t **margin = malloc(sizeof(int64_t *) * n);
    for (int i = 0; i < n; i++) {
        margin[i] = malloc(sizeof(int64_t) * n);
        for (int j = 0; j < n; j++) margin[i][j] = i == j ? piles[i] : 0;
    }
    for (int length = 2; length <= n; length++) {
        for (int i = 0; i + length <= n; i++) {
            int j = i + length - 1;
            int64_t left = piles[i] - margin[i + 1][j];
            int64_t right = piles[j] - margin[i][j - 1];
            margin[i][j] = left > right ? left : right;
        }
    }
    int answer = margin[0][n - 1] > 0;
    for (int i = 0; i < n; i++) free(margin[i]);
    free(margin);
    return answer;
}

static int64_t seed = 877;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_piles(int64_t *piles, int64_t limit) {
    int64_t total = 0;
    for (int i = 0; i < 500; i++) {
        piles[i] = next_random() % limit + 1;
        total += piles[i];
    }
    if (total % 2 == 0) piles[0] = piles[0] == limit ? piles[0] - 1 : piles[0] + 1;
}

int main(void) {
    static int64_t rows[20][500];
    for (int k = 0; k < 20; k++) random_piles(rows[k], k % 2 == 0 ? 500 : 3);
    int64_t wins = 0, check = 0;
    for (int k = 0; k < 1000; k++) {
        int answer = stone_game(rows[k % 20], 500);
        if (answer) wins++;
        check = (check * 3 + (answer ? 1 : 2)) % 1000000007;
    }
    printf("1000 games of 500 piles: Alice wins %lld, checksum %lld\n", (long long)wins, (long long)check);
    return 0;
}
