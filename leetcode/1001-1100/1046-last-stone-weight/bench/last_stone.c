// LeetCode #1046: Last Stone Weight -- benchmark driver, C mirror of
// last_stone.kara. C has no standard heap, so this is a largest-first
// binary heap in an array: built bottom-up in O(n), then popped and pushed
// as the ★ arm's queue does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void sift_down(int64_t *h, int64_t len, int64_t i) {
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, top = i;
        if (l < len && h[l] > h[top]) top = l;
        if (r < len && h[r] > h[top]) top = r;
        if (top == i) return;
        int64_t t = h[i];
        h[i] = h[top];
        h[top] = t;
        i = top;
    }
}

static void sift_up(int64_t *h, int64_t i) {
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (h[p] >= h[i]) return;
        int64_t t = h[i];
        h[i] = h[p];
        h[p] = t;
        i = p;
    }
}

// Floyd's pop, as the ★ arm's queue does it since kara 5bd3da78cc: the
// last element goes to the root, the root's slot walks down to a leaf
// along the larger child (the right one on a tie), one comparison a level,
// and the element carried there sifts back up.
static int64_t pop(int64_t *h, int64_t *len) {
    int64_t top = h[0];
    h[0] = h[--*len];
    int64_t n = *len, i = 0, c = 1, t;
    while (c + 1 < n) {
        c += h[c] <= h[c + 1];
        t = h[i];
        h[i] = h[c];
        h[c] = t;
        i = c;
        c = 2 * i + 1;
    }
    if (c + 1 == n) {
        t = h[i];
        h[i] = h[c];
        h[c] = t;
        i = c;
    }
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (h[i] <= h[p]) break;
        t = h[i];
        h[i] = h[p];
        h[p] = t;
        i = p;
    }
    return top;
}

static int64_t last_stone_weight(const int64_t *stones, int64_t n) {
    int64_t *h = malloc(n * sizeof(int64_t));
    memcpy(h, stones, n * sizeof(int64_t));
    int64_t len = n;
    for (int64_t i = n / 2 - 1; i >= 0; i--) sift_down(h, len, i);
    int64_t answer;
    for (;;) {
        if (len == 0) { answer = 0; break; }
        int64_t y = pop(h, &len);
        if (len == 0) { answer = y; break; }
        int64_t x = pop(h, &len);
        if (y > x) {
            h[len] = y - x;
            sift_up(h, len++);
        }
    }
    free(h);
    return answer;
}

static int64_t seed = 1046;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 1000, N = 3000, ROUNDS = 3 };
    int64_t *piles = malloc((int64_t)COUNT * N * sizeof(int64_t));
    for (int64_t c = 0; c < COUNT; c++)
        for (int64_t i = 0; i < N; i++) {
            int64_t high = next_random();
            int64_t low = next_random();
            piles[c * N + i] = (high * 32768 + low) % 1000000000 + 1;
        }
    int64_t total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int64_t c = 0; c < COUNT; c++) {
            int64_t answer = last_stone_weight(piles + c * N, N);
            total += answer;
            check = (check * 131 + answer % 1000000007 + 1) % 1000000007;
        }
    printf("%d piles of %d stones, %d rounds: total %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)total,
           (long long)check);
    free(piles);
    return 0;
}
