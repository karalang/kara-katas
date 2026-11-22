// LeetCode #2792: Count Nodes That Are Great Enough -- the bench in C:
// the ★ arm over 20 random trees of 10^4 nodes with values up to 10^4
// and k = 10, all drawn first, then each answered 20 times. Each node's
// k least values sit in a fixed row of K slots, sorted by qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 20
#define N 10000
#define K 10

static int64_t seed = 2792;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t order[N], stack_[N], least[N][K], held[N];

static int64_t count_great_enough_nodes(const int64_t *vals, const int64_t *left, const int64_t *right, int64_t n, int64_t k) {
    int64_t top = 0, len = 0;
    stack_[top++] = 0;
    while (top > 0) {
        int64_t u = stack_[--top];
        order[len++] = u;
        if (left[u] >= 0) stack_[top++] = left[u];
        if (right[u] >= 0) stack_[top++] = right[u];
    }
    int64_t great = 0;
    int64_t mine[2 * K + 1];
    for (int64_t j = n - 1; j >= 0; j--) {
        int64_t u = order[j], m = 0;
        mine[m++] = vals[u];
        int64_t kids[2] = {left[u], right[u]};
        for (int s = 0; s < 2; s++) {
            int64_t c = kids[s];
            if (c >= 0)
                for (int64_t i = 0; i < held[c]; i++) mine[m++] = least[c][i];
        }
        qsort(mine, m, sizeof(int64_t), cmp);
        if (m > k) m = k;
        if (m == k && mine[k - 1] < vals[u]) great++;
        for (int64_t i = 0; i < m; i++) least[u][i] = mine[i];
        held[u] = m;
    }
    return great;
}

static int64_t vals_[COUNT][N], left_[COUNT][N], right_[COUNT][N];

int main(void) {
    int rounds = 20;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) vals_[c][i] = next_random() % 10000 + 1;
        for (int i = 0; i < N; i++) left_[c][i] = right_[c][i] = -1;
        for (int64_t i = 1; i < N; i++) {
            for (;;) {
                int64_t p = next_random() % i;
                if (next_random() % 2 == 0) {
                    if (left_[c][p] < 0) { left_[c][p] = i; break; }
                } else if (right_[c][p] < 0) { right_[c][p] = i; break; }
            }
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = count_great_enough_nodes(vals_[c], left_[c], right_[c], N, K);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d trees of 10^4, %d rounds: great enough sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
