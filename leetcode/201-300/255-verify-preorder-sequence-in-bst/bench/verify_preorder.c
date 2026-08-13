// Benchmark workload for LeetCode #255 — Verify Preorder Sequence in BST (C mirror).
// Mirrors verify_preorder.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int main(void) {
    long n = 200000, rounds = 250;
    long *val = malloc(n * sizeof(long)), *left = malloc(n * sizeof(long)), *right = malloc(n * sizeof(long));
    long cnt = 0, state = 255255;

    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long v = state;
        if (cnt == 0) { val[cnt]=v; left[cnt]=-1; right[cnt]=-1; cnt++; }
        else {
            long cur = 0; int placed = 0;
            while (!placed) {
                if (v == val[cur]) placed = 1;
                else if (v < val[cur]) {
                    if (left[cur] == -1) { val[cnt]=v; left[cnt]=-1; right[cnt]=-1; left[cur]=cnt; cnt++; placed=1; }
                    else cur = left[cur];
                } else {
                    if (right[cur] == -1) { val[cnt]=v; left[cnt]=-1; right[cnt]=-1; right[cur]=cnt; cnt++; placed=1; }
                    else cur = right[cur];
                }
            }
        }
    }

    long *preorder = malloc(cnt * sizeof(long)); long m = 0;
    long *walk = malloc((cnt + 1) * sizeof(long)); long wn = 0;
    walk[wn++] = 0;
    while (wn > 0) {
        long node = walk[--wn];
        if (node != -1) {
            preorder[m++] = val[node];
            if (right[node] != -1) walk[wn++] = right[node];
            if (left[node] != -1) walk[wn++] = left[node];
        }
    }

    long *stack = malloc(m * sizeof(long));
    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        long sn = 0, lower = LONG_MIN; int ok = 1;
        for (long k = 0; k < m; k++) {
            long x = preorder[k];
            if (x < lower) ok = 0;
            while (sn > 0 && stack[sn-1] < x) lower = stack[--sn];
            stack[sn++] = x;
        }
        sink = ok ? (sink * 31 + 1) % 1000000007L : (sink * 31) % 1000000007L;
        sink = (sink * 131 + (lower % 1000000007L)) % 1000000007L;
    }
    printf("%ld %ld\n", m, sink);
    free(val); free(left); free(right); free(preorder); free(walk); free(stack);
    return 0;
}
