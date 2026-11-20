// LeetCode #2406: Divide Intervals Into Minimum Number of Groups -- the
// bench, the ★ arm in C: the intervals copied and sorted by left end with
// `qsort`, and a binary min-heap of each group's last right end.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

typedef struct { int64_t left, right; } interval;

static int64_t seed = 2406;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int by_ends(const void *a, const void *b) {
    const interval *x = a, *y = b;
    if (x->left != y->left) return x->left < y->left ? -1 : 1;
    if (x->right != y->right) return x->right < y->right ? -1 : 1;
    return 0;
}

static int64_t heap[N];

static void sift_down(int64_t n) {
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < n && heap[l] < heap[m]) m = l;
        if (r < n && heap[r] < heap[m]) m = r;
        if (m == i) return;
        int64_t t = heap[i]; heap[i] = heap[m]; heap[m] = t;
        i = m;
    }
}

static void push(int64_t *n, int64_t v) {
    int64_t i = (*n)++;
    heap[i] = v;
    while (i > 0 && heap[(i - 1) / 2] > heap[i]) {
        int64_t p = (i - 1) / 2, t = heap[i];
        heap[i] = heap[p]; heap[p] = t;
        i = p;
    }
}

static int64_t min_groups(const interval *iv, int64_t n) {
    interval *order = malloc(n * sizeof *order);
    memcpy(order, iv, n * sizeof *order);
    qsort(order, n, sizeof *order, by_ends);
    int64_t size = 0;
    for (int64_t i = 0; i < n; i++) {
        if (size > 0 && heap[0] < order[i].left) {
            heap[0] = heap[--size];
            sift_down(size);
        }
        push(&size, order[i].right);
    }
    free(order);
    return size;
}

int main(void) {
    static interval sets[10][N];
    for (int64_t i = 0; i < 10; i++)
        for (int j = 0; j < N; j++) {
            int64_t left = 1 + (next_random() * 32768 + next_random()) % 900000;
            sets[i][j].left = left;
            sets[i][j].right = left + (next_random() * 32768 + next_random()) % (1 + 1000 * i);
        }
    int64_t check = 0;
    for (int64_t p = 0; p < 5; p++)
        for (int i = 0; i < 10; i++) check = (check * 31 + min_groups(sets[i], N) + p) % 1000000007;
    printf("5 passes over 10 sets of 10^5 intervals: checksum %lld\n", (long long)check);
    return 0;
}
