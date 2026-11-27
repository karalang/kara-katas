// LeetCode #1834: Single-Threaded CPU -- the bench in C: the ★ arm over
// 50 calls on the first 50000 to 99999 of one list of 10^5 tasks, built once,
// each coming in at 1 to 10^6 and taking 1 to 10^4, each run's length drawn
// from the checksum so far. Each call copies its run, a list of two-number
// lists, as the arm takes its list by value, and the order is folded into
// the checksum.
// C has no priority queue, so the arm's queue is a binary heap of
// (processing time, index) written out, as the C solutions write it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t processing, index; } Ready;

static int64_t **sort_tasks;

static int by_enqueue(const void *a, const void *b) {
    int64_t i = *(const int64_t *)a, j = *(const int64_t *)b;
    int64_t x = sort_tasks[i][0], y = sort_tasks[j][0];
    if (x != y) return x < y ? -1 : 1;
    return i < j ? -1 : i > j;
}

static int less(Ready a, Ready b) {
    return a.processing < b.processing || (a.processing == b.processing && a.index < b.index);
}

static void push(Ready *heap, int64_t *len, Ready r) {
    int64_t k = (*len)++;
    heap[k] = r;
    while (k > 0 && less(heap[k], heap[(k - 1) / 2])) {
        Ready t = heap[k]; heap[k] = heap[(k - 1) / 2]; heap[(k - 1) / 2] = t;
        k = (k - 1) / 2;
    }
}

static Ready pop(Ready *heap, int64_t *len) {
    Ready top = heap[0];
    heap[0] = heap[--*len];
    int64_t k = 0;
    for (;;) {
        int64_t least = k, l = 2 * k + 1, r = 2 * k + 2;
        if (l < *len && less(heap[l], heap[least])) least = l;
        if (r < *len && less(heap[r], heap[least])) least = r;
        if (least == k) break;
        Ready t = heap[k]; heap[k] = heap[least]; heap[least] = t;
        k = least;
    }
    return top;
}

static int64_t *get_order(int64_t **tasks, int64_t n) {
    int64_t *coming = malloc(n * sizeof *coming);
    for (int64_t i = 0; i < n; i++) coming[i] = i;
    sort_tasks = tasks;
    qsort(coming, n, sizeof *coming, by_enqueue);
    Ready *ready = malloc(n * sizeof *ready);
    int64_t len = 0;
    int64_t *order = malloc(n * sizeof *order);
    int64_t done = 0, clock = 0, next = 0;
    while (done < n) {
        if (len == 0 && clock < tasks[coming[next]][0]) clock = tasks[coming[next]][0];
        while (next < n && tasks[coming[next]][0] <= clock) {
            int64_t i = coming[next];
            push(ready, &len, (Ready){tasks[i][1], i});
            next++;
        }
        Ready r = pop(ready, &len);
        clock += r.processing;
        order[done++] = r.index;
    }
    free(coming);
    free(ready);
    return order;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1834;
    int64_t **base = malloc(100000 * sizeof *base);
    for (int64_t k = 0; k < 100000; k++) {
        int64_t hi = next_random(&seed);
        base[k] = malloc(2 * sizeof **base);
        base[k][0] = 1 + (hi * 32768 + next_random(&seed)) % 1000000;
        base[k][1] = 1 + next_random(&seed) % 10000;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 50; call++) {
        int64_t n = 50000 + (check + call) % 50000;
        int64_t **run = malloc(n * sizeof *run);
        for (int64_t k = 0; k < n; k++) {
            run[k] = malloc(2 * sizeof **run);
            run[k][0] = base[k][0];
            run[k][1] = base[k][1];
        }
        int64_t *order = get_order(run, n);
        for (int64_t k = 0; k < n; k++) check = (check * 31 + order[k] + 1) % 1000000007;
        for (int64_t k = 0; k < n; k++) free(run[k]);
        free(run);
        free(order);
    }
    printf("50 calls: checksum %lld\n", (long long)check);
    return 0;
}
