// LeetCode #1606: Find Servers That Handled Most Number of Requests -- the
// bench in C, mirroring servers.kara. C has no ordered set, so the free
// servers are a segment tree of counts (first free at or after `start`, in
// O(log k)); the busy ones are a binary min-heap of (time free, server).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define PROBLEMS 20
#define REQUESTS 100000
#define K 10000

typedef struct { int64_t t; int s; } Busy;

static int size;      // leaves, a power of two >= k
static int *tree;     // tree[node] = free servers under node

static void tree_set(int s, int v) {
    int node = size + s;
    tree[node] = v;
    for (node /= 2; node >= 1; node /= 2) tree[node] = tree[2 * node] + tree[2 * node + 1];
}

// the first free server at or after `from`, or -1
static int first_free_from(int node, int lo, int hi, int from) {
    if (hi <= from || tree[node] == 0) return -1;
    if (node >= size) return lo;
    int mid = (lo + hi) / 2;
    int r = first_free_from(2 * node, lo, mid, from);
    if (r >= 0) return r;
    return first_free_from(2 * node + 1, mid, hi, from);
}

static Busy *heap;
static int heap_len;

static int less(Busy a, Busy b) { return a.t < b.t || (a.t == b.t && a.s < b.s); }

static void heap_push(Busy b) {
    int i = heap_len++;
    heap[i] = b;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (!less(heap[i], heap[p])) break;
        Busy x = heap[i]; heap[i] = heap[p]; heap[p] = x;
        i = p;
    }
}

static Busy heap_pop(void) {
    Busy top = heap[0];
    heap[0] = heap[--heap_len];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < heap_len && less(heap[l], heap[m])) m = l;
        if (r < heap_len && less(heap[r], heap[m])) m = r;
        if (m == i) break;
        Busy x = heap[i]; heap[i] = heap[m]; heap[m] = x;
        i = m;
    }
    return top;
}

// writes the busiest servers to out, returns how many
static int busiest_servers(int k, const int *arrival, const int *load, int n, int *out) {
    size = 1;
    while (size < k) size *= 2;
    tree = calloc(2 * size, sizeof(int));
    heap = malloc(n * sizeof(Busy));
    heap_len = 0;
    int *handled = calloc(k, sizeof(int));
    for (int s = 0; s < k; s++) tree[size + s] = 1;
    for (int node = size - 1; node >= 1; node--) tree[node] = tree[2 * node] + tree[2 * node + 1];
    for (int i = 0; i < n; i++) {
        int64_t now = arrival[i];
        while (heap_len > 0 && heap[0].t <= now) tree_set(heap_pop().s, 1);
        int s = first_free_from(1, 0, size, i % k);
        if (s < 0) s = first_free_from(1, 0, size, 0);
        if (s >= 0) {
            tree_set(s, 0);
            heap_push((Busy){now + load[i], s});
            handled[s]++;
        }
    }
    int most = 0;
    for (int s = 0; s < k; s++) if (handled[s] > most) most = handled[s];
    int m = 0;
    for (int s = 0; s < k; s++) if (handled[s] == most) out[m++] = s;
    free(handled); free(heap); free(tree);
    return m;
}

static int64_t seed = 1606;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int *arrival = malloc(sizeof(int) * PROBLEMS * REQUESTS);
    int *load = malloc(sizeof(int) * PROBLEMS * REQUESTS);
    for (int p = 0; p < PROBLEMS; p++) {
        int64_t t = 0;
        for (int i = 0; i < REQUESTS; i++) {
            t += next_random() % 3 + 1;
            arrival[p * REQUESTS + i] = (int)t;
            int64_t a = next_random();
            int64_t b = next_random();
            load[p * REQUESTS + i] = (int)((a * 32768 + b) % 30000 + 1);
        }
    }
    int *out = malloc(sizeof(int) * K);
    int64_t check = 0, busiest = 0;
    for (int p = 0; p < PROBLEMS; p++) {
        int m = busiest_servers(K, arrival + p * REQUESTS, load + p * REQUESTS, REQUESTS, out);
        for (int j = 0; j < m; j++) check = (check * 31 + out[j] + 1) % 1000000007;
        busiest += m;
    }
    printf("20 problems of 10000 servers and 100000 requests: %lld busiest, checksum %lld\n",
           (long long)busiest, (long long)check);
    free(out); free(arrival); free(load);
    return 0;
}
