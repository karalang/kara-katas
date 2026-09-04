// Benchmark lane for LeetCode 314 — C mirror of bench/vertical.kara.
// Grow POOL random trees of NODES malloc'd nodes once, then PASSES vertical-order
// traversals (extent pass + level-frontier BFS into an offset-indexed array of
// growable rows), each on the tree the running checksum selects. Every column's
// length and every value is folded into the masked checksum.
#include <stdio.h>
#include <stdlib.h>

#define POOL 8
#define NODES 50000
#define PASSES 240
#define MASK 1073741823LL

typedef struct Node { long long val; struct Node *left, *right; } Node;

static long long lcg(long long s) { return (s * 1103515245LL + 12345LL) & 0x7fffffffLL; }

static Node* grow(long long n, long long* seed) {
    if (n <= 0) return NULL;
    *seed = lcg(*seed);
    long long v = *seed % 1000 - 500;
    *seed = lcg(*seed);
    long long left_n = n <= 1 ? 0 : *seed % n;
    long long right_n = n - 1 - left_n;
    Node* l = grow(left_n, seed);
    Node* r = grow(right_n, seed);
    Node* t = malloc(sizeof(Node));
    t->val = v; t->left = l; t->right = r;
    return t;
}

static void extent(Node* t, long long col, long long* lo, long long* hi) {
    if (!t) return;
    if (col < *lo) *lo = col;
    if (col > *hi) *hi = col;
    extent(t->left, col - 1, lo, hi);
    extent(t->right, col + 1, lo, hi);
}

typedef struct { long long* data; long long len, cap; } Row;
typedef struct { Node* n; long long c; } Item;
typedef struct { Item* data; long long len, cap; } Frontier;

static void row_push(Row* r, long long v) {
    if (r->len == r->cap) { r->cap = r->cap ? r->cap * 2 : 4; r->data = realloc(r->data, r->cap * sizeof(long long)); }
    r->data[r->len++] = v;
}
static void fr_push(Frontier* f, Node* n, long long c) {
    if (f->len == f->cap) { f->cap = f->cap ? f->cap * 2 : 4; f->data = realloc(f->data, f->cap * sizeof(Item)); }
    f->data[f->len].n = n; f->data[f->len].c = c; f->len++;
}

// Returns the rows (caller frees); *ncols receives the column count.
static Row* vertical_order(Node* root, long long* ncols) {
    *ncols = 0;
    if (!root) return NULL;
    long long lo = 0, hi = 0;
    extent(root, 0, &lo, &hi);
    *ncols = hi - lo + 1;
    Row* out = calloc(*ncols, sizeof(Row));
    Frontier current = { NULL, 0, 0 };
    fr_push(&current, root, 0);
    while (current.len > 0) {
        Frontier next = { NULL, 0, 0 };
        for (long long i = 0; i < current.len; i++) {
            Node* n = current.data[i].n;
            long long c = current.data[i].c;
            row_push(&out[c - lo], n->val);
            if (n->left) fr_push(&next, n->left, c - 1);
            if (n->right) fr_push(&next, n->right, c + 1);
        }
        free(current.data);
        current = next;
    }
    free(current.data);
    return out;
}

int main(void) {
    long long seed = 314159;
    Node* pool[POOL];
    for (int i = 0; i < POOL; i++) pool[i] = grow(NODES, &seed);

    long long checksum = 0;
    for (int pass = 0; pass < PASSES; pass++) {
        long long which = checksum % POOL;
        long long ncols;
        Row* cols = vertical_order(pool[which], &ncols);
        checksum = (checksum + ncols) & MASK;
        for (long long i = 0; i < ncols; i++) {
            checksum = (checksum * 31 + cols[i].len) & MASK;
            for (long long j = 0; j < cols[i].len; j++)
                checksum = (checksum + cols[i].data[j] + 500) & MASK;
            free(cols[i].data);
        }
        free(cols);
    }
    printf("checksum %lld\n", checksum);
    return 0;
}
