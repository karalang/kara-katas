// LeetCode #2773: Height of Special Binary Tree -- the bench in C: the ★
// arm over 20 random trees of 10^4 nodes, all drawn first, then each
// answered 200 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 20
#define N 10000

static int64_t seed = 2773;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t depth(int64_t u, const int64_t *left, const int64_t *right) {
    int64_t best = 0;
    int64_t l = left[u];
    if (l >= 0 && right[l] != u) {
        int64_t d = depth(l, left, right) + 1;
        if (d > best) best = d;
    }
    int64_t r = right[u];
    if (r >= 0 && left[r] != u) {
        int64_t d = depth(r, left, right) + 1;
        if (d > best) best = d;
    }
    return best;
}

static int64_t lefts[COUNT][N], rights[COUNT][N];
static int64_t leaves[N], stack[N];

static void grown(int64_t *left, int64_t *right, int64_t n, int64_t reach) {
    for (int64_t i = 0; i < n; i++) left[i] = right[i] = -1;
    for (int64_t k = 1; k < n; k++) {
        int64_t span = reach < k ? reach : k;
        int64_t p = k - 1 - next_random() % span;
        while (left[p] >= 0 && right[p] >= 0) p = next_random() % k;
        int go_left;
        if (left[p] >= 0) go_left = 0;
        else if (right[p] >= 0) go_left = 1;
        else go_left = next_random() % 2 == 0;
        if (go_left) left[p] = k;
        else right[p] = k;
    }
    // the leaves, left to right, joined into a ring
    int64_t k = 0, top = 0;
    stack[top++] = 0;
    while (top > 0) {
        int64_t u = stack[--top];
        if (left[u] < 0 && right[u] < 0) leaves[k++] = u;
        if (right[u] >= 0) stack[top++] = right[u];
        if (left[u] >= 0) stack[top++] = left[u];
    }
    for (int64_t i = 0; i < k; i++) {
        right[leaves[i]] = leaves[(i + 1) % k];
        left[leaves[i]] = leaves[(i + k - 1) % k];
    }
}

int main(void) {
    int rounds = 200;
    for (int c = 0; c < COUNT; c++) {
        int64_t reach = next_random() % 50 + 1;
        grown(lefts[c], rights[c], N, reach);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t h = depth(0, lefts[c], rights[c]);
            total += h;
            check = (check * 31 + h + r) % 1000000007;
        }
    }
    printf("%d trees of 10^4, %d rounds: heights sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
