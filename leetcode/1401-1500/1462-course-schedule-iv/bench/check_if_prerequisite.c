// LeetCode #1462 bench in C: the ★ arm (the closure of the prerequisites
// by Floyd-Warshall) on the same 400 cases of 100 courses and 10^4
// queries.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define C 100
#define Q 10000

static void check_if_prerequisite(int n, int (*pre)[2], int m, int (*qs)[2], int q, char *out) {
    static char before[C][C];
    for (int u = 0; u < n; u++)
        for (int v = 0; v < n; v++) before[u][v] = 0;
    for (int i = 0; i < m; i++) before[pre[i][0]][pre[i][1]] = 1;
    for (int k = 0; k < n; k++)
        for (int u = 0; u < n; u++)
            if (before[u][k])
                for (int v = 0; v < n; v++)
                    if (before[k][v]) before[u][v] = 1;
    for (int i = 0; i < q; i++) out[i] = before[qs[i][0]][qs[i][1]];
}

static int64_t seed = 1462;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int pres[400][C * C / 2][2], counts[400], qss[400][Q][2];
    for (int c = 0; c < 400; c++) {
        int order[C];
        for (int i = 0; i < C; i++) order[i] = i;
        for (int i = C - 1; i >= 1; i--) {
            int j = (int)(next_random() % (i + 1));
            int t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        int m = 0;
        for (int i = 0; i < C; i++)
            for (int j = i + 1; j < C; j++)
                if (next_random() % 20 == 0) {
                    pres[c][m][0] = order[i];
                    pres[c][m][1] = order[j];
                    m++;
                }
        counts[c] = m;
        int q = 0;
        while (q < Q) {
            int u = (int)(next_random() % C), v = (int)(next_random() % C);
            if (u != v) {
                qss[c][q][0] = u;
                qss[c][q][1] = v;
                q++;
            }
        }
    }
    static char out[Q];
    int64_t check = 0;
    for (int c = 0; c < 400; c++) {
        check_if_prerequisite(C, pres[c], counts[c], qss[c], Q, out);
        for (int i = 0; i < Q; i++) check = (check * 3 + (out[i] ? 2 : 1)) % 1000000007;
    }
    printf("400 cases of 100 courses and 10^4 queries: checksum %lld\n", (long long)check);
    return 0;
}
