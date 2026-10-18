// LeetCode #699: Falling Squares -- bench program, C mirror of the segment-tree arm.
#include <stdio.h>
#include <stdlib.h>

static long long seed = 699;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long *best, *pending;

static long long max(long long a, long long b) { return a > b ? a : b; }

static void push_down(long long node) {
    long long p = pending[node];
    if (p >= 0) {
        best[2 * node] = p;
        pending[2 * node] = p;
        best[2 * node + 1] = p;
        pending[2 * node + 1] = p;
        pending[node] = -1;
    }
}

static long long query(long long node, long long lo, long long hi, long long from, long long to) {
    if (to <= lo || hi <= from) return 0;
    if (from <= lo && hi <= to) return best[node];
    push_down(node);
    long long mid = (lo + hi) / 2;
    return max(query(2 * node, lo, mid, from, to), query(2 * node + 1, mid, hi, from, to));
}

static void set(long long node, long long lo, long long hi, long long from, long long to, long long h) {
    if (to <= lo || hi <= from) return;
    if (from <= lo && hi <= to) {
        best[node] = h;
        pending[node] = h;
        return;
    }
    push_down(node);
    long long mid = (lo + hi) / 2;
    set(2 * node, lo, mid, from, to, h);
    set(2 * node + 1, mid, hi, from, to, h);
    best[node] = max(best[2 * node], best[2 * node + 1]);
}

static int cmp(const void *a, const void *b) {
    long long x = *(const long long *)a, y = *(const long long *)b;
    return (x > y) - (x < y);
}

static long long find(const long long *edges, long long n, long long x) {
    long long lo = 0, hi = n;
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (edges[mid] < x) lo = mid + 1; else hi = mid;
    }
    return lo;
}

// Writes the answer after each drop into heights.
static void falling_squares(const long long (*pos)[2], long long n, long long *heights) {
    long long *edges = malloc(2 * n * sizeof(long long));
    for (long long i = 0; i < n; i++) {
        edges[2 * i] = pos[i][0];
        edges[2 * i + 1] = pos[i][0] + pos[i][1];
    }
    qsort(edges, 2 * n, sizeof(long long), cmp);
    long long cells = 0;
    for (long long i = 0; i < 2 * n; i++)
        if (cells == 0 || edges[cells - 1] != edges[i]) edges[cells++] = edges[i];
    best = calloc(4 * cells, sizeof(long long));
    pending = malloc(4 * cells * sizeof(long long));
    for (long long i = 0; i < 4 * cells; i++) pending[i] = -1;
    for (long long i = 0; i < n; i++) {
        long long from = find(edges, cells, pos[i][0]);
        long long to = find(edges, cells, pos[i][0] + pos[i][1]);
        long long top = query(1, 0, cells, from, to) + pos[i][1];
        set(1, 0, cells, from, to, top);
        heights[i] = best[1];
    }
    free(edges);
    free(best);
    free(pending);
}

int main(void) {
    static long long problems[100][1000][2];
    for (long long p = 0; p < 100; p++) {
        long long width = 1000 + p * 999990;
        long long biggest = 1 + next_random() % 1000000;
        for (int i = 0; i < 1000; i++) {
            long long a = next_random();
            long long b = next_random();
            problems[p][i][0] = 1 + (a * 32768 + b) % width;
            problems[p][i][1] = 1 + next_random() % biggest;
        }
    }
    int rounds = 5;
    long long total = 0, checksum = 0;
    long long *heights = malloc(1000 * sizeof(long long));
    for (int r = 0; r < rounds; r++)
        for (int p = 0; p < 100; p++) {
            falling_squares((const long long (*)[2])problems[p], 1000, heights);
            long long last = heights[999];
            total += last;
            checksum = (checksum * 31 + last) % 1000000007;
        }
    free(heights);
    printf("%d rounds of 100 problems of 1000 squares: tallest stacks sum to %lld, checksum %lld\n", rounds, total, checksum);
    return 0;
}
