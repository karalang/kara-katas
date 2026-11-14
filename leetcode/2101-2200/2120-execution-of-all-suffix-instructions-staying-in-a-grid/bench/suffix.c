// LeetCode #2120: Execution of All Suffix Instructions Staying in a Grid
// -- the benchmark, the same algorithm as suffix.kara: each suffix
// simulated, 40 grids built once, 20 rounds with every start one row
// lower than in the round before.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *execute_instructions(int64_t n, const int64_t *start_pos, const char *s, int64_t m) {
    int64_t *answer = malloc(sizeof(int64_t) * (size_t)m);
    for (int64_t i = 0; i < m; i++) {
        int64_t row = start_pos[0], col = start_pos[1], count = 0;
        for (int64_t j = i; j < m; j++) {
            switch (s[j]) {
            case 'L': col -= 1; break;
            case 'R': col += 1; break;
            case 'U': row -= 1; break;
            default: row += 1; break;
            }
            if (row < 0 || row >= n || col < 0 || col >= n) break;
            count += 1;
        }
        answer[i] = count;
    }
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2120;
    int64_t ns[40], rows[40], cols[40];
    char moves[40][500];
    for (int g = 0; g < 40; g++) {
        ns[g] = next_random(&seed) % 401 + 100;
        rows[g] = next_random(&seed) % ns[g];
        cols[g] = next_random(&seed) % ns[g];
        for (int k = 0; k < 500; k++) moves[g][k] = "LRUD"[next_random(&seed) % 4];
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 20; round++) {
        for (int g = 0; g < 40; g++) {
            int64_t start[2] = {(rows[g] + round) % ns[g], cols[g]};
            int64_t *answer = execute_instructions(ns[g], start, moves[g], 500);
            for (int k = 0; k < 500; k++) {
                total += answer[k];
                check = (check * 31 + answer[k]) % 1000000007;
            }
            free(answer);
        }
    }
    printf("800 solves: %lld moves, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
