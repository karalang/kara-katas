// LeetCode #1601: Maximum Number of Achievable Transfer Requests
// -- the bench in C, mirroring transfers.kara: every subset of the
// requests as a bit mask, a subset no larger than the best skipped, a
// fresh malloc'd array of net changes per mask (as Kāra's Vec.filled is),
// on 100 problems of 16 requests among 6 buildings, all drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t maximum_requests(int32_t n, int32_t (*requests)[2], int r) {
    int32_t best = 0;
    for (int64_t mask = 0; mask < (1LL << r); mask++) {
        int32_t size = __builtin_popcountll(mask);
        if (size <= best) continue;
        int64_t *net = calloc(n, sizeof(int64_t));
        for (int i = 0; i < r; i++) {
            if (mask >> i & 1) {
                net[requests[i][0]]--;
                net[requests[i][1]]++;
            }
        }
        int ok = 1;
        for (int b = 0; b < n; b++)
            if (net[b] != 0) ok = 0;
        free(net);
        if (ok) best = size;
    }
    return best;
}

int main(void) {
    enum { P = 100, R = 16 };
    int64_t seed = 1601;
    int32_t (*problems)[R][2] = malloc(sizeof(int32_t[R][2]) * P);
    for (int p = 0; p < P; p++) {
        for (int i = 0; i < R; i++) {
            for (int k = 0; k < 2; k++) {
                seed = (seed * 1103515245 + 12345) % 2147483648LL;
                problems[p][i][k] = (int32_t)(seed / 65536 % 6);
            }
        }
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < P; p++) {
        int32_t answer = maximum_requests(6, problems[p], R);
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("100 problems of 16 requests among 6 buildings: total %lld, checksum %lld\n", (long long)total, (long long)check);
    free(problems);
    return 0;
}
