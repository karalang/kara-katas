// Benchmark for #427: mirror of quad_tree.kara (divide, then merge).
// Every node is malloc'd, as the Kāra `shared enum` is reference counted
// on the heap; four merged leaves are freed and replaced by one, and the
// tree is freed after it is counted.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Quad {
    int leaf;
    int val;
    struct Quad *kids[4];  // top left, top right, bottom left, bottom right
} Quad;

#define N 64
static int64_t grid[N][N];

static Quad *new_leaf(int val) {
    Quad *q = malloc(sizeof *q);
    q->leaf = 1;
    q->val = val;
    return q;
}

static Quad *build(int64_t row, int64_t col, int64_t size) {
    if (size == 1) return new_leaf(grid[row][col] == 1);
    int64_t half = size / 2;
    Quad *k0 = build(row, col, half);
    Quad *k1 = build(row, col + half, half);
    Quad *k2 = build(row + half, col, half);
    Quad *k3 = build(row + half, col + half, half);
    if (k0->leaf && k1->leaf && k2->leaf && k3->leaf &&
        k0->val == k1->val && k1->val == k2->val && k2->val == k3->val) {
        int v = k0->val;
        free(k0); free(k1); free(k2); free(k3);
        return new_leaf(v);
    }
    Quad *q = malloc(sizeof *q);
    q->leaf = 0;
    q->val = 1;
    q->kids[0] = k0; q->kids[1] = k1; q->kids[2] = k2; q->kids[3] = k3;
    return q;
}

static int64_t count_and_free(Quad *q) {
    int64_t total = 1;
    if (!q->leaf)
        for (int i = 0; i < 4; i++) total += count_and_free(q->kids[i]);
    free(q);
    return total;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t n = N;
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 20000;
    int64_t seed = 427;
    int64_t total = 0, checksum = 0;
    for (int64_t i = 0; i < rounds; i++) {
        int64_t size = (int64_t)1 << (step(&seed) % 7);
        int64_t top = step(&seed) % (n / size) * size;
        int64_t left = step(&seed) % (n / size) * size;
        int64_t v = step(&seed) % 2;
        for (int64_t r = top; r < top + size; r++)
            for (int64_t c = left; c < left + size; c++) grid[r][c] = v;
        int64_t r = step(&seed) % n;
        int64_t c = step(&seed) % n;
        grid[r][c] = 1 - grid[r][c];
        int64_t nodes = count_and_free(build(0, 0, n));
        total += nodes;
        checksum = (checksum * 31 + nodes) % 1000000007;
    }
    printf("%lld rounds on a %lld by %lld grid: %lld nodes, checksum %lld\n", (long long)rounds, (long long)n, (long long)n, (long long)total, (long long)checksum);
    return 0;
}
