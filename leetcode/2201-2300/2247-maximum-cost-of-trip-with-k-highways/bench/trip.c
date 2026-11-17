// LeetCode #2247: Maximum Cost of Trip With K Highways -- the benchmark's
// C mirror of trip.kara: dynamic programming over subsets, masks in
// increasing order, the roads in one array by offsets (CSR).
#include <stdint.h>
#include <stdio.h>

#define N 15
#define M 50

static int64_t best[1 << N][N];
static int64_t hw[M][3];
static int64_t start[N + 1], to[2 * M], toll[2 * M], fill[N];

static int64_t maximum_cost(int n, int m, int k) {
    if (k + 1 > n) return -1;
    for (int v = 0; v <= n; v++) start[v] = 0;
    for (int i = 0; i < m; i++) {
        start[hw[i][0] + 1]++;
        start[hw[i][1] + 1]++;
    }
    for (int v = 0; v < n; v++) start[v + 1] += start[v];
    for (int v = 0; v < n; v++) fill[v] = start[v];
    for (int i = 0; i < m; i++) {
        int64_t a = hw[i][0], b = hw[i][1];
        to[fill[a]] = b;
        toll[fill[a]++] = hw[i][2];
        to[fill[b]] = a;
        toll[fill[b]++] = hw[i][2];
    }
    int full = 1 << n;
    for (int mask = 0; mask < full; mask++)
        for (int v = 0; v < n; v++) best[mask][v] = -1;
    for (int v = 0; v < n; v++) best[1 << v][v] = 0;
    int64_t answer = -1;
    for (int mask = 1; mask < full; mask++) {
        int cities = __builtin_popcount(mask);
        for (int v = 0; v < n; v++) {
            int64_t cost = best[mask][v];
            if (cost < 0) continue;
            if (cities == k + 1) {
                if (cost > answer) answer = cost;
                continue;
            }
            for (int64_t e = start[v]; e < start[v + 1]; e++) {
                int64_t w = to[e];
                if ((mask & (1 << w)) == 0) {
                    int next = mask | (1 << w);
                    if (cost + toll[e] > best[next][w]) best[next][w] = cost + toll[e];
                }
            }
        }
    }
    return answer;
}

static int64_t seed = 2247;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 16; t++) {
        int64_t pairs[105][2];
        int count = 0;
        for (int a = 0; a < 15; a++)
            for (int b = a + 1; b < 15; b++) {
                pairs[count][0] = a;
                pairs[count++][1] = b;
            }
        for (int i = count - 1; i >= 1; i--) {
            int j = (int)(next_random() % (i + 1));
            int64_t x = pairs[i][0], y = pairs[i][1];
            pairs[i][0] = pairs[j][0];
            pairs[i][1] = pairs[j][1];
            pairs[j][0] = x;
            pairs[j][1] = y;
        }
        for (int i = 0; i < M; i++) {
            hw[i][0] = pairs[i][0];
            hw[i][1] = pairs[i][1];
            hw[i][2] = next_random() % 101;
        }
        check = (check * 31 + maximum_cost(15, M, 14) + 1) % 1000000007;
    }
    printf("16 maps of 15 cities: checksum %lld\n", (long long)check);
    return 0;
}
