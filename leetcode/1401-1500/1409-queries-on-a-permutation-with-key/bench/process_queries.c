// LeetCode #1409 bench, C: the same P, each query found and the part up to
// it turned one place, workload and checksum as process_queries.kara.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define M 1000
#define N 1000

static void process_queries(const int32_t *queries, int n, int m, int32_t *answer) {
    int32_t p[M];
    for (int i = 0; i < m; i++) {
        p[i] = i + 1;
    }
    for (int k = 0; k < n; k++) {
        int at = 0;
        while (p[at] != queries[k]) {
            at++;
        }
        answer[k] = at;
        memmove(p + 1, p, sizeof(int32_t) * at);
        p[0] = queries[k];
    }
}

int main(void) {
    int64_t seed = 1409, check = 0;
    int32_t queries[N], answer[N];
    for (int r = 0; r < 300; r++) {
        for (int k = 0; k < N; k++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            queries[k] = (int32_t)(1 + seed / 65536 % 1000);
        }
        process_queries(queries, N, M, answer);
        for (int k = 0; k < N; k++) {
            check = (check * 131 + answer[k]) % 1000000007;
        }
    }
    printf("300 rounds of 10^3 queries: checksum %lld\n", (long long)check);
    return 0;
}
