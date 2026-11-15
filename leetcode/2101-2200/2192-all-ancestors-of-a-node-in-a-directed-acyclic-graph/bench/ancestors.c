// benchmark's C mirror of ancestors.kara (LeetCode #2192, the ★ arm): a
// walk down from every node by a stack, the children in flat arrays.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1000
#define E 2000

static long long seed = 2192;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// children of each node from the edge list, as offsets into one array
static void get_ancestors(const long long (*edges)[2], long long *first, long long *kids,
                          long long *count, long long *anc, char *seen, long long *stack) {
    memset(first, 0, sizeof(long long) * (N + 1));
    for (int i = 0; i < E; i++) first[edges[i][0] + 1]++;
    for (int v = 0; v < N; v++) first[v + 1] += first[v];
    long long fill[N];
    memcpy(fill, first, sizeof fill);
    for (int i = 0; i < E; i++) kids[fill[edges[i][0]]++] = edges[i][1];
    memset(count, 0, sizeof(long long) * N);
    for (long long start = 0; start < N; start++) {
        memset(seen, 0, N);
        seen[start] = 1;
        long long top = 0;
        stack[top++] = start;
        while (top > 0) {
            long long u = stack[--top];
            for (long long k = first[u]; k < first[u + 1]; k++) {
                long long v = kids[k];
                if (!seen[v]) {
                    seen[v] = 1;
                    anc[v * N + count[v]++] = start;
                    stack[top++] = v;
                }
            }
        }
    }
}

int main(void) {
    static long long dags[20][E][2];
    for (int d = 0; d < 20; d++) {
        long long order[N];
        for (int i = 0; i < N; i++) order[i] = i;
        for (int i = N - 1; i >= 1; i--) {
            long long j = next_random() % (i + 1);
            long long t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        int e = 0;
        while (e < E) {
            long long a = next_random() % N, b = next_random() % N;
            if (a < b) {
                dags[d][e][0] = order[a];
                dags[d][e][1] = order[b];
                e++;
            } else if (b < a) {
                dags[d][e][0] = order[b];
                dags[d][e][1] = order[a];
                e++;
            }
        }
    }
    long long *first = malloc(sizeof(long long) * (N + 1));
    long long *kids = malloc(sizeof(long long) * E);
    long long *count = malloc(sizeof(long long) * N);
    long long *anc = malloc(sizeof(long long) * N * N);
    char *seen = malloc(N);
    long long *stack = malloc(sizeof(long long) * N);
    long long check = 0;
    for (int r = 0; r < 2000; r++) {
        get_ancestors((const long long (*)[2])dags[r % 20], first, kids, count, anc, seen, stack);
        for (int v = 0; v < N; v++) {
            check = (check * 31 + count[v]) % 1000000007;
            for (long long i = 0; i < count[v]; i++) check = (check * 31 + anc[v * N + i] + 1) % 1000000007;
        }
    }
    printf("2000 solves: checksum %lld\n", check);
    free(first);
    free(kids);
    free(count);
    free(anc);
    free(seen);
    free(stack);
    return 0;
}
