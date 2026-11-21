// LeetCode #2492: Minimum Score of a Path Between Two Cities -- C mirror
// of the benchmark (score.kara): the same map, passes and checksum, the
// breadth-first search over adjacency lists built afresh on every ask.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2492;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct { int64_t to, distance; } Edge;

static int64_t min_score(int64_t n, int64_t m, int64_t (*roads)[3]) {
    int64_t *start = calloc(n + 2, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        start[roads[i][0] + 1]++;
        start[roads[i][1] + 1]++;
    }
    for (int64_t c = 1; c <= n + 1; c++) start[c] += start[c - 1];
    int64_t *fill = malloc((n + 1) * sizeof(int64_t));
    for (int64_t c = 0; c <= n; c++) fill[c] = start[c];
    Edge *edges = malloc(2 * m * sizeof(Edge));
    for (int64_t i = 0; i < m; i++) {
        int64_t a = roads[i][0], b = roads[i][1], d = roads[i][2];
        edges[fill[a]++] = (Edge){b, d};
        edges[fill[b]++] = (Edge){a, d};
    }
    char *seen = calloc(n + 1, 1);
    int64_t *queue = malloc((n + 1) * sizeof(int64_t));
    int64_t len = 0, head = 0, least = INT64_MAX;
    queue[len++] = 1;
    seen[1] = 1;
    while (head < len) {
        int64_t city = queue[head++];
        for (int64_t e = start[city]; e < start[city + 1]; e++) {
            if (edges[e].distance < least) least = edges[e].distance;
            if (!seen[edges[e].to]) {
                seen[edges[e].to] = 1;
                queue[len++] = edges[e].to;
            }
        }
    }
    free(start); free(fill); free(edges); free(seen); free(queue);
    return least;
}

int main(void) {
    const int64_t n = 100000, passes = 50;
    int64_t (*roads)[3] = malloc(n * sizeof *roads);
    int64_t m = 0;
    roads[m][0] = 1; roads[m][1] = n; roads[m][2] = 10000; m++;
    while (m < n) {
        int64_t a = (next_random() * 32768 + next_random()) % n + 1;
        int64_t b = (next_random() * 32768 + next_random()) % n + 1;
        if (a != b) {
            roads[m][0] = a; roads[m][1] = b; roads[m][2] = next_random() % 10000 + 1; m++;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t at = check % m;
        int64_t was = roads[at][2];
        roads[at][2] = (check / m + p) % 10000 + 1;
        check = (check * 31 + min_score(n, m, roads) + p) % 1000000007;
        roads[at][2] = was;
    }
    printf("%lld passes over 10^5 cities and %lld roads: checksum %lld\n",
           (long long)passes, (long long)m, (long long)check);
    free(roads);
    return 0;
}
