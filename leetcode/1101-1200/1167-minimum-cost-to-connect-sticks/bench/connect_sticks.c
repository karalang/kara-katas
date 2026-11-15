// LeetCode #1167: Minimum Cost to Connect Sticks -- the ★ arm's bench in C:
// a binary min-heap in an array, built in O(n), the two shortest joined and
// the join pushed back.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void sift_down(int64_t *h, int64_t n, int64_t i) {
    for (;;) {
        int64_t l = 2 * i + 1, m = i;
        if (l < n && h[l] < h[m]) m = l;
        if (l + 1 < n && h[l + 1] < h[m]) m = l + 1;
        if (m == i) return;
        int64_t t = h[i];
        h[i] = h[m];
        h[m] = t;
        i = m;
    }
}

static int64_t pop(int64_t *h, int64_t *n) {
    int64_t top = h[0];
    h[0] = h[--*n];
    sift_down(h, *n, 0);
    return top;
}

static void push(int64_t *h, int64_t *n, int64_t x) {
    int64_t i = (*n)++;
    h[i] = x;
    while (i > 0 && h[(i - 1) / 2] > h[i]) {
        int64_t p = (i - 1) / 2, t = h[i];
        h[i] = h[p];
        h[p] = t;
        i = p;
    }
}

static int64_t connect_sticks(const int64_t *sticks, int64_t n) {
    int64_t *h = malloc(n * sizeof(int64_t));
    memcpy(h, sticks, n * sizeof(int64_t));
    for (int64_t i = n / 2 - 1; i >= 0; i--) sift_down(h, n, i);
    int64_t cost = 0;
    while (n > 1) {
        int64_t a = pop(h, &n);
        int64_t b = pop(h, &n);
        cost += a + b;
        push(h, &n, a + b);
    }
    free(h);
    return cost;
}

static int64_t seed = 1167;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t piles[16][10000];
    for (int k = 0; k < 16; k++)
        for (int i = 0; i < 10000; i++) piles[k][i] = 1 + next_random() % 10000;
    int64_t total = 0, check = 0;
    for (int r = 0; r < 40; r++) {
        for (int k = 0; k < 16; k++) {
            int64_t at = next_random() % 10000;
            piles[k][at] = 1 + next_random() % 10000;
            int64_t c = connect_sticks(piles[k], 10000);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    printf("40 rounds over 16 piles of 10^4 sticks: total %lld, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
