// Benchmark workload for LeetCode #261 — Graph Valid Tree (C mirror).
// Mirrors valid_tree.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>

static long find(long *parent, long x) {
    long r = x;
    while (parent[r] != r) r = parent[r];
    long c = x;
    while (parent[c] != r) {
        long nxt = parent[c];
        parent[c] = r;
        c = nxt;
    }
    return r;
}

int main(void) {
    long n = 100000, rounds = 240, m = n - 1;

    long *eu = malloc(m * sizeof(long));
    long *ev = malloc(m * sizeof(long));
    long state = 261261;
    for (long i = 1; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        eu[i - 1] = (state / 65536L) % i;
        ev[i - 1] = i;
    }
    for (long sh = m - 1; sh > 0; sh--) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long j = (state / 65536L) % (sh + 1);
        long tu = eu[sh]; eu[sh] = eu[j]; eu[j] = tu;
        long tv = ev[sh]; ev[sh] = ev[j]; ev[j] = tv;
    }

    long *parent = malloc(n * sizeof(long));
    long *size = malloc(n * sizeof(long));

    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        for (long k = 0; k < n; k++) { parent[k] = k; size[k] = 1; }

        long start = (r * 7919L) % m;
        long components = n;
        int cyclic = 0;
        for (long e = 0; e < m; ) {
            long idx = (start + e) % m;
            long ra = find(parent, eu[idx]);
            long rb = find(parent, ev[idx]);
            if (ra == rb) { cyclic = 1; e = m; }
            else {
                if (size[ra] < size[rb]) { parent[ra] = rb; size[rb] += size[ra]; }
                else { parent[rb] = ra; size[ra] += size[rb]; }
                components--;
                e++;
            }
        }

        long acc = 0;
        for (long p = 0; p < n; p++) acc = (acc * 31 + parent[p]) % 1000000007L;
        long verdict = (components == 1 && !cyclic) ? 1 : 0;
        sink = (sink * 131 + acc + verdict) % 1000000007L;
    }

    printf("%ld\n", sink);
    free(eu); free(ev); free(parent); free(size);
    return 0;
}
