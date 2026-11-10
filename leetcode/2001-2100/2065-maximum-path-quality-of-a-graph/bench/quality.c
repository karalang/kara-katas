// LeetCode #2065: Maximum Path Quality of a Graph -- C mirror of the ★
// arm's benchmark (quality.kara): 1000 graphs of 1000 nodes, 2000 edges
// tried, each from a node to one of the next three and of time 10 or 11,
// and the time 100; a recursive search with a count of visits per node.
// A node has at most four edges, so the adjacency is four slots per node,
// and an edge already there is found by looking through them.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define N 1000
static int64_t values[N];
static int adj_to[N][4];
static int64_t adj_t[N][4];
static int degree[N];
static int64_t visits[N];
static int64_t best;

static void walk(int node, int64_t time, int64_t quality, int64_t max_time) {
    if (node == 0 && quality > best) best = quality;
    for (int k = 0; k < degree[node]; k++) {
        int next = adj_to[node][k];
        int64_t t = adj_t[node][k];
        if (time + t <= max_time) {
            visits[next]++;
            int64_t gain = visits[next] == 1 ? values[next] : 0;
            walk(next, time + t, quality + gain, max_time);
            visits[next]--;
        }
    }
}

static int64_t seed = 2065;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int g = 0; g < 1000; g++) {
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            values[i] = (hi * 32768 + next_random()) % 100000001;
        }
        memset(degree, 0, sizeof degree);
        for (int e = 0; e < 2000; e++) {
            int u = (int)(next_random() % N);
            int v = (int)((u + 1 + next_random() % 3) % N);
            int64_t t = next_random() % 2 + 10;
            int fresh = 1;
            for (int k = 0; k < degree[u]; k++)
                if (adj_to[u][k] == v) fresh = 0;
            if (degree[u] < 4 && degree[v] < 4 && fresh) {
                adj_to[u][degree[u]] = v;
                adj_t[u][degree[u]++] = t;
                adj_to[v][degree[v]] = u;
                adj_t[v][degree[v]++] = t;
            }
        }
        memset(visits, 0, sizeof visits);
        visits[0] = 1;
        best = 0;
        walk(0, 0, values[0], 100);
        total += best;
        check = (check * 31 + best % 1000000007) % 1000000007;
    }
    printf("1000 graphs: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
