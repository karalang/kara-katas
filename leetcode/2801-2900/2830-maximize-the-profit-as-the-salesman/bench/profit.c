// LeetCode #2830: Maximize the Profit as the Salesman -- the bench's C
// mirror of the ★ arm: the offers filed by their last house, by a count
// and a prefix sum into one array, and best[i] the most gold from the
// first i houses.

#include <stdio.h>
#include <stdlib.h>

static long long maximize_the_profit(int n, const long long (*offers)[3], int m) {
    int *head = calloc(n + 1, sizeof *head);
    for (int j = 0; j < m; j++) head[offers[j][1] + 1]++;
    for (int i = 0; i < n; i++) head[i + 1] += head[i];
    int *fill = malloc(n * sizeof *fill), *order = malloc(m * sizeof *order);
    for (int i = 0; i < n; i++) fill[i] = head[i];
    for (int j = 0; j < m; j++) order[fill[offers[j][1]]++] = j;
    long long *best = malloc((n + 1) * sizeof *best);
    best[0] = 0;
    for (int i = 0; i < n; i++) {
        best[i + 1] = best[i];
        for (int t = head[i]; t < head[i + 1]; t++) {
            const long long *o = offers[order[t]];
            long long v = best[o[0]] + o[2];
            if (v > best[i + 1]) best[i + 1] = v;
        }
    }
    long long answer = best[n];
    free(head);
    free(fill);
    free(order);
    free(best);
    return answer;
}

static long long seed = 2830;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long wide(void) {
    long long a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    enum { COUNT = 20, ROUNDS = 10, N = 100000 };
    long long (*streets)[N][3] = malloc(sizeof(long long[COUNT][N][3]));
    for (int c = 0; c < COUNT; c++)
        for (int j = 0; j < N; j++) {
            long long start = wide() % N;
            long long end = start + next_random() % 100;
            if (end > N - 1) end = N - 1;
            streets[c][j][0] = start;
            streets[c][j][1] = end;
            streets[c][j][2] = next_random() % 1000 + 1;
        }
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            long long a = maximize_the_profit(N, (const long long (*)[3])streets[c], N);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    printf("%d streets of %d, %d rounds: gold totals %lld, checksum %lld\n", COUNT, N, ROUNDS, total, check);
    free(streets);
    return 0;
}
