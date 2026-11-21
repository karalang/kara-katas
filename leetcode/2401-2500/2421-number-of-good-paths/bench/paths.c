// LeetCode #2421: Number of Good Paths -- the bench, the ★ arm in C:
// union-find over the nodes in order of value, each value's nodes joined
// to their neighbours no larger and then counted by root. The adjacency
// is two arrays in compressed form, the order a stable merge sort by
// value, and each value's roots counted in an array indexed by root,
// cleared after the value, where the other languages use a hash map.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 30000

static int64_t seed = 2421;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static const int64_t *sort_vals;

static void merge_sort(int64_t *a, int64_t *tmp, int64_t n) {
    if (n < 2) return;
    int64_t h = n / 2;
    merge_sort(a, tmp, h);
    merge_sort(a + h, tmp, n - h);
    int64_t i = 0, j = h, k = 0;
    while (i < h && j < n) tmp[k++] = sort_vals[a[j]] < sort_vals[a[i]] ? a[j++] : a[i++];
    while (i < h) tmp[k++] = a[i++];
    while (j < n) tmp[k++] = a[j++];
    memcpy(a, tmp, n * sizeof *a);
}

static int64_t number_of_good_paths(const int64_t *vals, const int64_t (*edges)[2], int64_t n) {
    int64_t *start = calloc(n + 1, sizeof *start);
    int64_t *next = malloc(2 * (n - 1) * sizeof *next + 1);
    for (int64_t e = 0; e < n - 1; e++) {
        start[edges[e][0] + 1]++;
        start[edges[e][1] + 1]++;
    }
    for (int64_t i = 0; i < n; i++) start[i + 1] += start[i];
    int64_t *fill = malloc(n * sizeof *fill);
    memcpy(fill, start, n * sizeof *fill);
    for (int64_t e = 0; e < n - 1; e++) {
        next[fill[edges[e][0]]++] = edges[e][1];
        next[fill[edges[e][1]]++] = edges[e][0];
    }
    int64_t *parent = malloc(n * sizeof *parent);
    int64_t *order = malloc(n * sizeof *order);
    int64_t *tmp = malloc(n * sizeof *tmp);
    int64_t *count = calloc(n, sizeof *count);
    for (int64_t i = 0; i < n; i++) parent[i] = order[i] = i;
    sort_vals = vals;
    merge_sort(order, tmp, n);
    int64_t good = n;
    int64_t i = 0;
    while (i < n) {
        int64_t j = i;
        while (j < n && vals[order[j]] == vals[order[i]]) j++;
        for (int64_t t = i; t < j; t++) {
            int64_t u = order[t];
            for (int64_t e = start[u]; e < start[u + 1]; e++) {
                int64_t v = next[e];
                if (vals[v] <= vals[u]) {
                    int64_t ru = find(parent, u);
                    int64_t rv = find(parent, v);
                    parent[ru] = rv;
                }
            }
        }
        for (int64_t t = i; t < j; t++) {
            int64_t c = ++count[find(parent, order[t])];
            good += c - 1;
        }
        for (int64_t t = i; t < j; t++) count[find(parent, order[t])] = 0;
        i = j;
    }
    free(start);
    free(next);
    free(fill);
    free(parent);
    free(order);
    free(tmp);
    free(count);
    return good;
}

int main(void) {
    static int64_t vals[10][N];
    static int64_t edges[10][N - 1][2];
    for (int64_t t = 0; t < 10; t++) {
        for (int64_t i = 0; i < N; i++) vals[t][i] = 1 + next_random() % (3 + 1000 * t);
        for (int64_t i = 1; i < N; i++) {
            edges[t][i - 1][0] = next_random() % i;
            edges[t][i - 1][1] = i;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++)
        for (int64_t t = 0; t < 10; t++) check = (check * 31 + number_of_good_paths(vals[t], (const int64_t (*)[2])edges[t], N) + p) % 1000000007;
    printf("20 passes over 10 trees of 3 * 10^4 nodes: checksum %lld\n", (long long)check);
    return 0;
}
