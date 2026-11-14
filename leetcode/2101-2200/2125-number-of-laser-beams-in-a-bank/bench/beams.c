// LeetCode #2125: Number of Laser Beams in a Bank -- the benchmark, the
// same algorithm as beams.kara; each row a 500-byte string.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BANKS 12
#define M 500
#define N 500

static int64_t seed = 2125;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t number_of_beams(char rows[M][N]) {
    int64_t prev = 0, beams = 0;
    for (int r = 0; r < M; r++) {
        int64_t devices = 0;
        for (int c = 0; c < N; c++) devices += rows[r][c] == '1';
        if (devices > 0) {
            beams += prev * devices;
            prev = devices;
        }
    }
    return beams;
}

int main(void) {
    char (*banks)[M][N] = malloc(sizeof(char[BANKS][M][N]));
    for (int b = 0; b < BANKS; b++)
        for (int r = 0; r < M; r++)
            for (int c = 0; c < N; c++)
                banks[b][r][c] = next_random() % 4 < b % 3 + 1 ? '1' : '0';
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 500; round++) {
        for (int b = 0; b < BANKS; b++) {
            int64_t r = next_random() % 500;
            int64_t c = next_random() % 500;
            banks[b][r][c] = banks[b][r][c] == '1' ? '0' : '1';
            int64_t beams = number_of_beams(banks[b]);
            total += beams;
            check = (check * 31 + beams + round) % 1000000007;
        }
    }
    printf("6000 solves: %lld beams, checksum %lld\n", (long long)total, (long long)check);
    free(banks);
    return 0;
}
