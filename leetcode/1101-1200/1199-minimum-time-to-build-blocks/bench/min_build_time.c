// LeetCode #1199 bench: the ★ arm in C, over the same 200 sets of 1000
// blocks and 50 rounds as the Kāra bench; the smallest-first queue is a
// binary heap in an array, built bottom up from a copy of the blocks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1000

static void sift_down(int64_t *h, int64_t n, int64_t i) {
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < n && h[l] < h[m]) m = l;
        if (r < n && h[r] < h[m]) m = r;
        if (m == i) return;
        int64_t t = h[i];
        h[i] = h[m];
        h[m] = t;
        i = m;
    }
}

static void sift_up(int64_t *h, int64_t i) {
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (h[p] <= h[i]) return;
        int64_t t = h[i];
        h[i] = h[p];
        h[p] = t;
        i = p;
    }
}

static int64_t pop(int64_t *h, int64_t *n) {
    int64_t top = h[0];
    h[0] = h[--*n];
    sift_down(h, *n, 0);
    return top;
}

static int64_t min_build_time(const int64_t *blocks, int64_t split, int64_t *heap) {
    int64_t n = N;
    memcpy(heap, blocks, N * sizeof(int64_t));
    for (int64_t i = n / 2 - 1; i >= 0; i--) sift_down(heap, n, i);
    while (n > 1) {
        pop(heap, &n);
        int64_t slower = pop(heap, &n);
        heap[n] = slower + split;
        sift_up(heap, n);
        n++;
    }
    return heap[0];
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t highs[3] = {10, 1000, 100000};
    int64_t seed = 1199;
    int64_t *blocks = malloc(200 * N * sizeof(int64_t));
    int64_t splits[200];
    int64_t *heap = malloc(N * sizeof(int64_t));
    for (int k = 0; k < 200; k++) {
        int64_t high = highs[k % 3];
        splits[k] = next_random(&seed) % 100 + 1;
        for (int j = 0; j < N; j++) {
            int64_t a = next_random(&seed);
            int64_t b = next_random(&seed);
            blocks[k * N + j] = (a * 32768 + b) % high + 1;
        }
    }
    int64_t check = 0;
    for (int r = 0; r < 50; r++) {
        for (int k = 0; k < 200; k++) {
            int64_t t = min_build_time(blocks + k * N, splits[k], heap);
            check = (check * 131 + t) % 1000000007;
        }
    }
    printf("50 rounds of 200 sets of 1000 blocks: checksum %lld\n", (long long)check);
    free(heap);
    free(blocks);
    return 0;
}
