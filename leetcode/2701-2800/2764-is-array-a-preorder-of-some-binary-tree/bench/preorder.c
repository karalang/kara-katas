// LeetCode #2764: Is Array a Preorder of Some Binary Tree -- the bench
// (preorder.kara in C): a stack of the nodes whose subtrees are still
// open, each node closing every subtree above its parent.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2764;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

static int is_preorder(const int64_t *nodes, int64_t n, int64_t *stack) {
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t id = nodes[2 * i], parent = nodes[2 * i + 1];
        while (top > 0 && stack[top - 1] != parent) top--;
        if (top == 0 && parent != -1) return 0;
        stack[top++] = id;
    }
    return 1;
}

// a random binary tree of n nodes, ids spread over 0 to 100000, listed in
// a random preorder; then, half the time, two places swapped
static void tree(int64_t n, int64_t *nodes) {
    int64_t shift = wide() % 100001;
    int64_t *ids = malloc(sizeof(int64_t) * n);
    int64_t *kids = malloc(sizeof(int64_t) * 2 * n);
    int64_t *nkids = calloc(n, sizeof(int64_t));
    int64_t *parent = malloc(sizeof(int64_t) * n);
    int64_t *stack = malloc(sizeof(int64_t) * n);
    for (int64_t k = 0; k < n; k++) ids[k] = (k * 37 + shift) % 100001;
    for (int64_t k = 1; k < n; k++) {
        int64_t p = wide() % k;
        while (nkids[p] == 2) p = wide() % k;
        kids[2 * p + nkids[p]++] = k;
    }
    for (int64_t k = 0; k < n; k++) parent[k] = -1;
    for (int64_t p = 0; p < n; p++)
        for (int64_t j = 0; j < nkids[p]; j++) parent[kids[2 * p + j]] = p;
    int64_t top = 0, at = 0;
    stack[top++] = 0;
    while (top > 0) {
        int64_t u = stack[--top];
        nodes[2 * at] = ids[u];
        nodes[2 * at + 1] = parent[u] >= 0 ? ids[parent[u]] : -1;
        at++;
        int64_t a = kids[2 * u], b = kids[2 * u + 1];
        if (nkids[u] == 2) {
            if (next_random() % 2 == 1) { int64_t t = a; a = b; b = t; }
            stack[top++] = b;
            stack[top++] = a;
        } else if (nkids[u] == 1) {
            stack[top++] = a;
        }
    }
    if (next_random() % 2 == 1 && n > 1) {
        int64_t i = wide() % n;
        int64_t j = wide() % n;
        int64_t t0 = nodes[2 * i], t1 = nodes[2 * i + 1];
        nodes[2 * i] = nodes[2 * j]; nodes[2 * i + 1] = nodes[2 * j + 1];
        nodes[2 * j] = t0; nodes[2 * j + 1] = t1;
    }
    free(ids); free(kids); free(nkids); free(parent); free(stack);
}

int main(void) {
    const int count = 20, rounds = 100;
    const int64_t n = 100000;
    int64_t *nodes = malloc(sizeof(int64_t) * 2 * n * count);
    int64_t *stack = malloc(sizeof(int64_t) * n);
    for (int c = 0; c < count; c++) tree(n, nodes + 2 * n * c);
    int64_t good = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int c = 0; c < count; c++)
            if (is_preorder(nodes + 2 * n * c, n, stack)) {
                good++;
                check = (check * 31 + c + r) % 1000000007;
            }
    printf("%d trees of 100000, %d rounds: %lld preorders, checksum %lld\n", count, rounds, (long long)good, (long long)check);
    free(nodes); free(stack);
    return 0;
}
