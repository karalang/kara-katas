// LeetCode #2876: Count Visited Nodes in a Directed Graph -- the bench,
// as visited.kara: 20 graphs of 10^5 nodes, each answered 20 times by
// the peeling arm. The work arrays are allocated per call, as the other
// languages allocate theirs.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *count_visited_nodes(const int64_t *edges, int64_t n) {
    int64_t *incoming = calloc(n, sizeof *incoming);
    int64_t *peeled = malloc(n * sizeof *peeled);
    int64_t *answer = calloc(n, sizeof *answer);
    int64_t *cycle = malloc(n * sizeof *cycle);
    for (int64_t u = 0; u < n; u++) incoming[edges[u]]++;
    int64_t len = 0;
    for (int64_t u = 0; u < n; u++)
        if (incoming[u] == 0) peeled[len++] = u;
    for (int64_t head = 0; head < len; head++) {
        int64_t w = edges[peeled[head]];
        if (--incoming[w] == 0) peeled[len++] = w;
    }
    for (int64_t start = 0; start < n; start++) {
        if (incoming[start] > 0 && answer[start] == 0) {
            int64_t m = 0;
            cycle[m++] = start;
            for (int64_t u = edges[start]; u != start; u = edges[u]) cycle[m++] = u;
            for (int64_t i = 0; i < m; i++) answer[cycle[i]] = m;
        }
    }
    for (int64_t i = len - 1; i >= 0; i--) answer[peeled[i]] = answer[edges[peeled[i]]] + 1;
    free(incoming);
    free(peeled);
    free(cycle);
    return answer;
}

static int64_t seed = 2876;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 20, rounds = 20, n = 100000;
    int64_t *graphs = malloc(count * n * sizeof *graphs);
    for (int64_t c = 0; c < count; c++)
        for (int64_t i = 0; i < n; i++)
            graphs[c * n + i] = c % 2 == 1 ? (i + next_random() % 5 + 1) % n : (i + wide() % (n - 1) + 1) % n;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t *counts = count_visited_nodes(graphs + c * n, n);
            for (int64_t u = 0; u < n; u++) total += counts[u];
            check = (check * 31 + counts[r] + counts[n - 1 - r]) % 1000000007;
            free(counts);
        }
    }
    printf("%lld graphs of %lld, %lld rounds: visits total %lld, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(graphs);
    return 0;
}
