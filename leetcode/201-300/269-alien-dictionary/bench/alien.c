// Benchmark workload for LeetCode #269 — Alien Dictionary (C mirror).
// Mirrors alien.kara algorithm-for-algorithm, including the flat corpus and the
// hoisted working structures (see that file for why).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { long *d; long n, cap; } Vec;
static void vpush(Vec *v, long x) {
    if (v->n == v->cap) { v->cap = v->cap ? v->cap * 2 : 64; v->d = realloc(v->d, v->cap * sizeof(long)); }
    v->d[v->n++] = x;
}

int main(void) {
    long lists = 20000, rounds = 60, alpha = 8;

    Vec letters = {0}, wstart = {0}, wlen = {0}, lstart = {0}, lcount = {0};
    long state = 269269;

    for (long li = 0; li < lists; li++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long m = (state / 65536L) % 5 + 2;

        long rank[8];
        for (long z = 0; z < alpha; z++) rank[z] = z;
        for (long sh = alpha - 1; sh > 0; sh--) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long j = (state / 65536L) % (sh + 1);
            long t = rank[sh]; rank[sh] = rank[j]; rank[j] = t;
        }

        long buf[64], st[8], ln[8], bn = 0;
        for (long wi = 0; wi < m; wi++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long L = (state / 65536L) % 4 + 1;
            st[wi] = bn; ln[wi] = L;
            for (long p = 0; p < L; p++) {
                state = (state * 1103515245L + 12345L) & 2147483647L;
                buf[bn++] = (state / 65536L) % alpha;
            }
        }

        for (long a = 1; a < m; a++) {
            long b = a;
            while (b > 0) {
                long s1 = st[b-1], n1 = ln[b-1], s2 = st[b], n2 = ln[b];
                long lim = n2 < n1 ? n2 : n1;
                long k = 0; int swap = 0, decided = 0;
                while (k < lim) {
                    if (buf[s1+k] != buf[s2+k]) {
                        if (rank[buf[s1+k]] > rank[buf[s2+k]]) swap = 1;
                        decided = 1; k = lim;
                    } else k++;
                }
                if (!decided && n1 > n2) swap = 1;
                if (swap) {
                    long ts = st[b-1]; st[b-1] = st[b]; st[b] = ts;
                    long tl = ln[b-1]; ln[b-1] = ln[b]; ln[b] = tl;
                    b--;
                } else b = 0;
            }
        }

        state = (state * 1103515245L + 12345L) & 2147483647L;
        if ((state / 65536L) % 2 == 0 && m >= 2) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long at = (state / 65536L) % (m - 1);
            long ts = st[at]; st[at] = st[at+1]; st[at+1] = ts;
            long tl = ln[at]; ln[at] = ln[at+1]; ln[at+1] = tl;
        }

        vpush(&lstart, wstart.n);
        vpush(&lcount, m);
        for (long q = 0; q < m; q++) {
            vpush(&wstart, letters.n);
            vpush(&wlen, ln[q]);
            for (long r = 0; r < ln[q]; r++) vpush(&letters, buf[st[q] + r]);
        }
    }

    char adj[676];
    long indeg[26];
    char present[26], done[26];

    long sink = 0;
    for (long r0 = 0; r0 < rounds; r0++) {
        for (long idx = 0; idx < lists; idx++) {
            long base = lstart.d[idx], n = lcount.d[idx];

            for (long c = 0; c < 26; c++) { indeg[c] = 0; present[c] = 0; done[c] = 0; }
            memset(adj, 0, sizeof adj);

            for (long w = 0; w < n; w++) {
                long s = wstart.d[base + w], L = wlen.d[base + w];
                for (long p = 0; p < L; p++) present[letters.d[s + p]] = 1;
            }

            int bad = 0;
            long p2 = 0;
            while (p2 + 1 < n) {
                long s1 = wstart.d[base+p2], n1 = wlen.d[base+p2];
                long s2 = wstart.d[base+p2+1], n2 = wlen.d[base+p2+1];
                long lim = n2 < n1 ? n2 : n1;
                long k = 0; int found = 0;
                while (k < lim) {
                    long x = letters.d[s1+k], y = letters.d[s2+k];
                    if (x != y) {
                        if (!adj[x*26+y]) { adj[x*26+y] = 1; indeg[y]++; }
                        found = 1; k = lim;
                    } else k++;
                }
                if (!found && n1 > n2) { bad = 1; p2 = n; } else p2++;
            }

            long acc = 0;
            if (!bad) {
                long remaining = 0;
                for (long d = 0; d < 26; d++) if (present[d]) remaining++;
                long placed = 0;
                while (placed < remaining) {
                    long pick = -1;
                    for (long s3 = 0; s3 < 26; ) {
                        if (present[s3] && !done[s3] && indeg[s3] == 0) { pick = s3; s3 = 26; }
                        else s3++;
                    }
                    if (pick < 0) { acc = 0; placed = remaining; }
                    else {
                        done[pick] = 1;
                        acc = (acc * 31 + pick + 1) % 1000000007L;
                        placed++;
                        for (long t = 0; t < 26; t++) if (adj[pick*26+t]) indeg[t]--;
                    }
                }
            }
            sink = (sink * 131 + acc) % 1000000007L;
        }
    }
    printf("%ld\n", sink);
    return 0;
}
