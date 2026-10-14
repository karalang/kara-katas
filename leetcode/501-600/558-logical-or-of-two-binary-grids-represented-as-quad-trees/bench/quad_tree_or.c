// Benchmark for #558: C mirror of the ★ arm (recursion, then a merge);
// see quad_tree_or.kara. The Kāra `shared enum` is reference counted on
// the heap, so a node here is malloc'd with a count: the answer shares
// the subtrees it keeps with the two trees, four merged leaves are
// released and replaced by one, and the answer is released after it is
// counted.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Quad {
    int64_t refs;
    bool leaf;
    bool val;
    struct Quad *kids[4];  // top left, top right, bottom left, bottom right
} Quad;

static Quad *retain(Quad *q) {
    q->refs++;
    return q;
}

static void release(Quad *q) {
    if (--q->refs > 0) return;
    if (!q->leaf)
        for (int i = 0; i < 4; i++) release(q->kids[i]);
    free(q);
}

static Quad *new_leaf(bool v) {
    Quad *q = malloc(sizeof *q);
    q->refs = 1;
    q->leaf = true;
    q->val = v;
    return q;
}

// Takes ownership of the four children.
static Quad *new_split(Quad *k0, Quad *k1, Quad *k2, Quad *k3) {
    if (k0->leaf && k1->leaf && k2->leaf && k3->leaf && k0->val == k1->val &&
        k1->val == k2->val && k2->val == k3->val) {
        bool v = k0->val;
        release(k0); release(k1); release(k2); release(k3);
        return new_leaf(v);
    }
    Quad *q = malloc(sizeof *q);
    q->refs = 1;
    q->leaf = false;
    q->val = true;
    q->kids[0] = k0; q->kids[1] = k1; q->kids[2] = k2; q->kids[3] = k3;
    return q;
}

static Quad *intersect(Quad *a, Quad *b) {
    if (a->leaf) return retain(a->val ? a : b);
    if (b->leaf) return retain(b->val ? b : a);
    Quad *k[4];
    for (int i = 0; i < 4; i++) k[i] = intersect(a->kids[i], b->kids[i]);
    return new_split(k[0], k[1], k[2], k[3]);
}

// ---- benchmark --------------------------------------------------------------

#define N 64
static int64_t grid[N][N];

static Quad *build(int row, int col, int size) {
    if (size == 1) return new_leaf(grid[row][col] == 1);
    int half = size / 2;
    Quad *k0 = build(row, col, half);
    Quad *k1 = build(row, col + half, half);
    Quad *k2 = build(row + half, col, half);
    Quad *k3 = build(row + half, col + half, half);
    return new_split(k0, k1, k2, k3);
}

static int64_t count(const Quad *q) {
    if (q->leaf) return 1;
    return 1 + count(q->kids[0]) + count(q->kids[1]) + count(q->kids[2]) + count(q->kids[3]);
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 200, ROUNDS = 300 };
    int64_t seed = 558;
    Quad *trees[COUNT];
    for (int t = 0; t < COUNT; t++) {
        int block = 1 << (step(&seed) % 5);
        for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++) grid[r][c] = 0;
        for (int br = 0; br < N / block; br++)
            for (int bc = 0; bc < N / block; bc++) {
                int64_t v = step(&seed) % 3 == 0 ? 1 : 0;
                for (int r = 0; r < block; r++)
                    for (int c = 0; c < block; c++) grid[br * block + r][bc * block + c] = v;
            }
        for (int f = 0; f < 40; f++) {
            int64_t r = step(&seed) % N;
            int64_t c = step(&seed) % N;
            grid[r][c] = 1 - grid[r][c];
        }
        trees[t] = build(0, 0, N);
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int i = 0; i < COUNT; i++) {
            int other = (i * 7 + round + 1) % COUNT;
            Quad *q = intersect(trees[i], trees[other]);
            int64_t nodes = count(q);
            release(q);
            total += nodes;
            checksum = (checksum * 31 + nodes) % 1000000007;
        }
    for (int t = 0; t < COUNT; t++) release(trees[t]);
    printf("%d trees, %d rounds: %lld nodes, checksum %lld\n", COUNT, ROUNDS, (long long)total,
           (long long)checksum);
    return 0;
}
