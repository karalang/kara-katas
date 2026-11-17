// LeetCode #1595: Minimum Cost to Connect Two Groups of Points
// -- the bench in C, mirroring connect.kara: one edge per first point
// over a mask of the second group's points joined, then each point still
// alone takes its cheapest edge; 200 problems of 12 by 12, costs from 0
// to 100, all drawn first. Each problem is a malloc'd array of malloc'd
// rows and each step's table a fresh malloc, as in Kāra.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 1595;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int32_t connect_two_groups(int32_t **cost, int first, int second) {
    int full = 1 << second;
    int32_t cheapest[32];
    for (int j = 0; j < second; j++) {
        cheapest[j] = cost[0][j];
        for (int i = 1; i < first; i++)
            if (cost[i][j] < cheapest[j]) cheapest[j] = cost[i][j];
    }
    int32_t *best = malloc(sizeof(int32_t) * full);
    for (int m = 0; m < full; m++) best[m] = INT32_MAX;
    best[0] = 0;
    for (int i = 0; i < first; i++) {
        int32_t *next = malloc(sizeof(int32_t) * full);
        for (int m = 0; m < full; m++) next[m] = INT32_MAX;
        for (int mask = 0; mask < full; mask++) {
            if (best[mask] == INT32_MAX) continue;
            for (int j = 0; j < second; j++) {
                int joined = mask | 1 << j;
                int32_t v = best[mask] + cost[i][j];
                if (v < next[joined]) next[joined] = v;
            }
        }
        free(best);
        best = next;
    }
    int32_t answer = INT32_MAX;
    for (int mask = 0; mask < full; mask++) {
        if (best[mask] == INT32_MAX) continue;
        int32_t total = best[mask];
        for (int j = 0; j < second; j++)
            if ((mask >> j & 1) == 0) total += cheapest[j];
        if (total < answer) answer = total;
    }
    free(best);
    return answer;
}

int main(void) {
    enum { N = 200, S = 12 };
    int32_t ***problems = malloc(sizeof(int32_t **) * N);
    for (int p = 0; p < N; p++) {
        problems[p] = malloc(sizeof(int32_t *) * S);
        for (int r = 0; r < S; r++) {
            problems[p][r] = malloc(sizeof(int32_t) * S);
            for (int c = 0; c < S; c++) problems[p][r][c] = (int32_t)(next_random() % 101);
        }
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < N; p++) {
        int32_t answer = connect_two_groups(problems[p], S, S);
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("200 problems of 12 by 12: total %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int p = 0; p < N; p++) {
        for (int r = 0; r < S; r++) free(problems[p][r]);
        free(problems[p]);
    }
    free(problems);
    return 0;
}
