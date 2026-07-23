#include <stdio.h>
#include <stdlib.h>

// Benchmark workload for LeetCode #210 — Course Schedule II.
//
// Build-once + punch: a large random DAG (edges always low->high index, so it is
// acyclic by construction) is built ONCE into CSR adjacency. Kahn's topological
// sort is then run PASSES times; each pass copies the base in-degrees, "punches"
// one course by inflating its in-degree so it (and everything downstream) is
// starved from the order — exactly the kata's cycle-becomes-partial-order path —
// and folds the emitted order into a checksum. The queue relaxation is a
// data-dependent scatter (indeg[nb]-- then a gated push) that does NOT vectorize.
// Sink = sum over passes of (emitted count + order checksum).

#define MOD 1000000007L
#define BIG 1000000L

int main(void) {
    long n = 20000;
    long e = 80000;
    long passes = 800;

    long *eb = malloc(e * sizeof(long));
    long *ea = malloc(e * sizeof(long));
    long *outdeg = calloc(n, sizeof(long));
    long *indeg0 = calloc(n, sizeof(long));

    long state = 12345;
    for (long i = 0; i < e; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long b = state % (n - 1);              // 0 .. n-2
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long a = b + 1 + state % (n - 1 - b);  // b+1 .. n-1  (b < a => DAG)
        eb[i] = b;
        ea[i] = a;
        outdeg[b]++;
        indeg0[a]++;
    }

    // CSR build.
    long *adj_start = malloc((n + 1) * sizeof(long));
    adj_start[0] = 0;
    for (long i = 0; i < n; i++) adj_start[i + 1] = adj_start[i] + outdeg[i];
    long *adj_flat = malloc(e * sizeof(long));
    long *cursor = malloc(n * sizeof(long));
    for (long i = 0; i < n; i++) cursor[i] = adj_start[i];
    for (long i = 0; i < e; i++) adj_flat[cursor[eb[i]]++] = ea[i];

    long *indeg = malloc(n * sizeof(long));
    long *queue = malloc(n * sizeof(long));

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        for (long i = 0; i < n; i++) indeg[i] = indeg0[i];
        long blocked = p % n;
        indeg[blocked] += BIG;

        long head = 0, tail = 0;
        for (long c = 0; c < n; c++) {
            if (indeg[c] == 0) queue[tail++] = c;
        }
        long checksum = 0, cnt = 0;
        while (head < tail) {
            long node = queue[head++];
            checksum = (checksum + node * (cnt + 1)) % MOD;
            cnt++;
            for (long j = adj_start[node]; j < adj_start[node + 1]; j++) {
                long nb = adj_flat[j];
                indeg[nb]--;
                if (indeg[nb] == 0) queue[tail++] = nb;
            }
        }
        sink += cnt + checksum;
    }

    printf("%ld\n", sink);
    free(eb); free(ea); free(outdeg); free(indeg0);
    free(adj_start); free(adj_flat); free(cursor); free(indeg); free(queue);
    return 0;
}
