#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n = 5000, m = 15000, passes = 8000;

    long *esrc = malloc(m * sizeof(long));
    long *edst = malloc(m * sizeof(long));
    long state = 12345;
    for (long e = 0; e < m; e++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long s = state % n;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long d = state % n;
        esrc[e] = s;
        edst[e] = d;
    }

    long *outdeg = calloc(n, sizeof(long));
    long *base_indeg = calloc(n, sizeof(long));
    for (long e = 0; e < m; e++) {
        outdeg[esrc[e]]++;
        base_indeg[edst[e]]++;
    }

    long *offset = malloc((n + 1) * sizeof(long));
    offset[0] = 0;
    long acc = 0;
    for (long c = 0; c < n; c++) {
        acc += outdeg[c];
        offset[c + 1] = acc;
    }

    long *adj = malloc(m * sizeof(long));
    long *cursor = malloc(n * sizeof(long));
    for (long c = 0; c < n; c++) cursor[c] = offset[c];
    for (long e = 0; e < m; e++) {
        long sidx = cursor[esrc[e]];
        adj[sidx] = edst[e];
        cursor[esrc[e]] = sidx + 1;
    }

    long *indeg = malloc(n * sizeof(long));
    long *queue = malloc(n * sizeof(long));

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        for (long c = 0; c < n; c++) indeg[c] = base_indeg[c];
        long blocked = p % n;
        indeg[blocked] += 1;

        long qt = 0;
        for (long c = 0; c < n; c++) {
            if (indeg[c] == 0) {
                queue[qt++] = c;
            }
        }

        long qh = 0, finished = 0;
        while (qh < qt) {
            long node = queue[qh++];
            finished++;
            long stop = offset[node + 1];
            for (long k = offset[node]; k < stop; k++) {
                long nb = adj[k];
                indeg[nb]--;
                if (indeg[nb] == 0) {
                    queue[qt++] = nb;
                }
            }
        }
        sink += finished;
    }
    printf("%ld\n", sink);
    free(esrc); free(edst); free(outdeg); free(base_indeg);
    free(offset); free(adj); free(cursor); free(indeg); free(queue);
    return 0;
}
