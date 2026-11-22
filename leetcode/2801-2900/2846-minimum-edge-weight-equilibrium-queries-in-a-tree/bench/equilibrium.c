// LeetCode #2846: Minimum Edge Weight Equilibrium Queries in a Tree --
// the bench, mirrored from equilibrium.kara: weight counts from the
// root by a breadth-first walk, and each query's lowest common ancestor
// by binary lifting; adjacency as a compressed array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LEVELS 15

static void min_operations_queries(long n, const int64_t *edges, long asked, const int64_t *queries, int64_t *answers) {
    long *deg = calloc(n + 1, sizeof(long));
    for (long i = 0; i < n - 1; i++) {
        deg[edges[3 * i]]++;
        deg[edges[3 * i + 1]]++;
    }
    long *start = malloc((n + 1) * sizeof(long));
    start[0] = 0;
    for (long v = 0; v < n; v++) start[v + 1] = start[v] + deg[v];
    long *fill = malloc(n * sizeof(long));
    memcpy(fill, start, n * sizeof(long));
    long *to = malloc(2 * (n - 1 + 1) * sizeof(long)), *wt = malloc(2 * (n - 1 + 1) * sizeof(long));
    for (long i = 0; i < n - 1; i++) {
        long u = edges[3 * i], v = edges[3 * i + 1], w = edges[3 * i + 2];
        to[fill[u]] = v;
        wt[fill[u]++] = w;
        to[fill[v]] = u;
        wt[fill[v]++] = w;
    }
    long *up = calloc(LEVELS * n, sizeof(long));
    int64_t *depth = calloc(n, sizeof(int64_t));
    int64_t *count = calloc(n * 27, sizeof(int64_t));
    char *seen = calloc(n, 1);
    long *queue = malloc(n * sizeof(long));
    long head = 0, tail = 0;
    seen[0] = 1;
    queue[tail++] = 0;
    while (head < tail) {
        long v = queue[head++];
        for (long e = start[v]; e < start[v + 1]; e++) {
            long u = to[e];
            if (!seen[u]) {
                seen[u] = 1;
                up[u] = v;
                depth[u] = depth[v] + 1;
                memcpy(count + u * 27, count + v * 27, 27 * sizeof(int64_t));
                count[u * 27 + wt[e]]++;
                queue[tail++] = u;
            }
        }
    }
    for (int j = 1; j < LEVELS; j++)
        for (long v = 0; v < n; v++) up[j * n + v] = up[(j - 1) * n + up[(j - 1) * n + v]];
    for (long q = 0; q < asked; q++) {
        long a = queries[2 * q], b = queries[2 * q + 1];
        long x = depth[a] >= depth[b] ? a : b, y = depth[a] >= depth[b] ? b : a;
        for (int j = LEVELS - 1; j >= 0; j--)
            if (depth[x] - (1 << j) >= depth[y]) x = up[j * n + x];
        long c;
        if (x == y) {
            c = x;
        } else {
            for (int j = LEVELS - 1; j >= 0; j--)
                if (up[j * n + x] != up[j * n + y]) {
                    x = up[j * n + x];
                    y = up[j * n + y];
                }
            c = up[x];
        }
        int64_t sum = 0, most = 0;
        for (int w = 1; w < 27; w++) {
            int64_t here = count[a * 27 + w] + count[b * 27 + w] - 2 * count[c * 27 + w];
            sum += here;
            if (here > most) most = here;
        }
        answers[q] = sum - most;
    }
    free(deg); free(start); free(fill); free(to); free(wt);
    free(up); free(depth); free(count); free(seen); free(queue);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 10, n = 10000, asked = 20000, rounds = 5;
    int64_t seed = 2846;
    int64_t *edges = malloc(count * (n - 1) * 3 * sizeof(int64_t));
    int64_t *queries = malloc(count * asked * 2 * sizeof(int64_t));
    int64_t *label = malloc(n * sizeof(int64_t));
    for (long c = 0; c < count; c++) {
        for (long i = 0; i < n; i++) label[i] = i;
        for (long i = n - 1; i >= 1; i--) {
            long j = next_random(&seed) % (i + 1);
            int64_t t = label[i];
            label[i] = label[j];
            label[j] = t;
        }
        int64_t *e = edges + c * (n - 1) * 3;
        for (long i = 1; i < n; i++) {
            e[3 * (i - 1)] = label[i];
            e[3 * (i - 1) + 1] = label[next_random(&seed) % i];
            e[3 * (i - 1) + 2] = next_random(&seed) % 26 + 1;
        }
        int64_t *q = queries + c * asked * 2;
        for (long i = 0; i < asked; i++) {
            q[2 * i] = next_random(&seed) % n;
            q[2 * i + 1] = next_random(&seed) % n;
        }
    }
    int64_t *answers = malloc(asked * sizeof(int64_t));
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            min_operations_queries(n, edges + c * (n - 1) * 3, asked, queries + c * asked * 2, answers);
            for (long i = 0; i < asked; i++) {
                total += answers[i];
                check = (check * 31 + answers[i] + r) % 1000000007;
            }
        }
    }
    printf("%ld trees of %ld, %ld queries, %ld rounds: %lld operations, checksum %lld\n", count, n, asked, rounds, (long long)total, (long long)check);
    free(edges); free(queries); free(label); free(answers);
    return 0;
}
