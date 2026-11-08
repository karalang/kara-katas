// LeetCode #1514: Path with Maximum Probability -- the bench: 10 graphs of
// 50000 nodes and 100000 edges built once, then 5 questions asked of each
// by the ★ arm: Dijkstra for the largest product on a binary heap. (The
// chance is never negative, so the cast truncating is the floor.)
#include <stdio.h>
#include <stdlib.h>

typedef struct { double chance; long node; } Entry;

static int above(Entry x, Entry y) {
    return x.chance > y.chance || (x.chance == y.chance && x.node > y.node);
}

static void push(Entry *h, long *len, Entry e) {
    long i = (*len)++;
    h[i] = e;
    while (i > 0 && above(h[i], h[(i - 1) / 2])) {
        Entry t = h[i]; h[i] = h[(i - 1) / 2]; h[(i - 1) / 2] = t;
        i = (i - 1) / 2;
    }
}

static Entry pop(Entry *h, long *len) {
    Entry top = h[0];
    h[0] = h[--(*len)];
    long i = 0;
    for (;;) {
        long l = 2 * i + 1, r = l + 1, m = i;
        if (l < *len && above(h[l], h[m])) m = l;
        if (r < *len && above(h[r], h[m])) m = r;
        if (m == i) break;
        Entry t = h[i]; h[i] = h[m]; h[m] = t;
        i = m;
    }
    return top;
}

static double max_probability(long n, long m, const long *ea, const long *eb, const double *prob, long start, long end) {
    long *deg = calloc(n + 1, sizeof(long));
    for (long i = 0; i < m; i++) { deg[ea[i] + 1]++; deg[eb[i] + 1]++; }
    for (long v = 0; v < n; v++) deg[v + 1] += deg[v];
    long *fill = malloc(n * sizeof(long));
    for (long v = 0; v < n; v++) fill[v] = deg[v];
    long *to = malloc(2 * m * sizeof(long));
    double *wt = malloc(2 * m * sizeof(double));
    for (long i = 0; i < m; i++) {
        to[fill[ea[i]]] = eb[i]; wt[fill[ea[i]]++] = prob[i];
        to[fill[eb[i]]] = ea[i]; wt[fill[eb[i]]++] = prob[i];
    }
    double *best = calloc(n, sizeof(double));
    best[start] = 1.0;
    Entry *heap = malloc((2 * m + 1) * sizeof(Entry));
    long len = 0;
    push(heap, &len, (Entry){1.0, start});
    double answer = 0.0;
    while (len > 0) {
        Entry e = pop(heap, &len);
        if (e.node == end) { answer = e.chance; break; }
        if (e.chance < best[e.node]) continue;
        for (long k = deg[e.node]; k < deg[e.node + 1]; k++) {
            double through = e.chance * wt[k];
            if (through > best[to[k]]) {
                best[to[k]] = through;
                push(heap, &len, (Entry){through, to[k]});
            }
        }
    }
    free(deg); free(fill); free(to); free(wt); free(best); free(heap);
    return answer;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static long wide(long *seed) {
    long hi = next_random(seed) * 32768;
    return hi + next_random(seed);
}

int main(void) {
    long seed = 1514, n = 50000, m = 100000;
    static long ea[10][100000], eb[10][100000];
    static double pr[10][100000];
    for (int g = 0; g < 10; g++) {
        for (long i = 0; i < m; i++) {
            long a = wide(&seed) % n;
            long b = (a + 1 + wide(&seed) % (n - 1)) % n;
            ea[g][i] = a; eb[g][i] = b;
            pr[g][i] = (double)(next_random(&seed) % 21 + 80) / 100.0;
        }
    }
    long check = 0;
    for (int r = 0; r < 5; r++) {
        for (int g = 0; g < 10; g++) {
            long start = wide(&seed) % n;
            long end = wide(&seed) % n;
            double p = max_probability(n, m, ea[g], eb[g], pr[g], start, end);
            check = (check * 31 + (long)(p * 1000000000000.0 + 0.5) + 1) % 1000000007;
        }
    }
    printf("50 questions over 10 graphs of 50000 nodes: checksum %ld\n", check);
    return 0;
}
