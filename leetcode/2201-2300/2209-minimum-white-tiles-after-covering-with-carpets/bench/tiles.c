// benchmark's C mirror of tiles.kara (LeetCode #2209, the ★ arm): a table
// best[j][i], the fewest white tiles left visible among the first i tiles
// with j carpets, filled row by row.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t minimum_white_tiles(const char *floor, long num_carpets, long carpet_len) {
    long n = (long)strlen(floor);
    int64_t *tiles = malloc(sizeof(int64_t) * n);
    for (long i = 0; i < n; i++) tiles[i] = floor[i] == '1' ? 1 : 0;
    int64_t **best = malloc(sizeof(int64_t *) * (num_carpets + 1));
    for (long j = 0; j <= num_carpets; j++) best[j] = calloc(n + 1, sizeof(int64_t));
    for (long j = 0; j <= num_carpets; j++) {
        for (long i = 1; i <= n; i++) {
            int64_t left = best[j][i - 1] + tiles[i - 1];
            if (j == 0) {
                best[j][i] = left;
            } else {
                long from = i - carpet_len > 0 ? i - carpet_len : 0;
                int64_t covered = best[j - 1][from];
                best[j][i] = left < covered ? left : covered;
            }
        }
    }
    int64_t answer = best[num_carpets][n];
    for (long j = 0; j <= num_carpets; j++) free(best[j]);
    free(best);
    free(tiles);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2209;
    char *floors[8];
    for (int f = 0; f < 8; f++) {
        int64_t white_in_8 = f % 7 + 1;
        floors[f] = malloc(1001);
        for (int i = 0; i < 1000; i++) floors[f][i] = next_random(&seed) % 8 < white_in_8 ? '1' : '0';
        floors[f][1000] = 0;
    }
    // each floor asked 40 times, carpets 10 to 249, each 1 to 20 long
    int64_t check = 0;
    for (long q = 0; q < 40; q++) {
        for (long f = 0; f < 8; f++) {
            long carpets = 10 + (q * 37 + f * 11) % 240;
            long len = 1 + (q * 7 + f * 3) % 20;
            check = (check * 31 + minimum_white_tiles(floors[f], carpets, len)) % 1000000007;
        }
    }
    printf("40 passes over 8 floors: checksum %lld\n", (long long)check);
    for (int f = 0; f < 8; f++) free(floors[f]);
    return 0;
}
