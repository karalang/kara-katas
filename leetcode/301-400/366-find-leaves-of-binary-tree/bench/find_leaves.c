// Benchmark for #366 -- mirror of find_leaves.kara. Tree nodes are
// heap-allocated with a reference count, as the shared enum's are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Tree {
    int64_t rc, v;
    struct Tree *left, *right; // NULL is the empty tree
} Tree;

typedef struct { int64_t len, cap, *a; } Vec;
static void push(Vec *x, int64_t v) {
    if (x->len == x->cap) { x->cap = x->cap ? x->cap * 2 : 4; x->a = realloc(x->a, (size_t)x->cap * 8); }
    x->a[x->len++] = v;
}

static int64_t n_nodes, *vals, *lft, *rgt;

static void links(const int64_t *items, const char *present, int64_t n) {
    n_nodes = 0;
    if (n == 0 || !present[0]) return;
    int64_t *queue = malloc((size_t)n * 8), qh = 0, qt = 0;
    vals[0] = items[0]; lft[0] = rgt[0] = -1; n_nodes = 1;
    queue[qt++] = 0;
    int64_t i = 1;
    while (i < n) {
        if (qh == qt) break;
        int64_t parent = queue[qh++];
        for (int side = 0; side < 2; side++) {
            if (i < n) {
                if (present[i]) {
                    int64_t id = n_nodes++;
                    vals[id] = items[i]; lft[id] = rgt[id] = -1;
                    if (side == 0) lft[parent] = id; else rgt[parent] = id;
                    queue[qt++] = id;
                }
                i++;
            }
        }
    }
    free(queue);
}

static Tree *build(int64_t id) {
    if (id < 0) return NULL;
    Tree *t = malloc(sizeof(Tree));
    t->rc = 1; t->v = vals[id];
    t->left = build(lft[id]);
    t->right = build(rgt[id]);
    return t;
}

static void release(Tree *t) {
    if (!t || --t->rc) return;
    release(t->left); release(t->right); free(t);
}

static Vec *out; static int64_t out_len, out_cap;

static int64_t file_by_height(const Tree *t) {
    if (!t) return -1;
    int64_t a = file_by_height(t->left), b = file_by_height(t->right);
    int64_t h = 1 + (a > b ? a : b);
    if (h == out_len) {
        if (out_len == out_cap) { out_cap = out_cap ? out_cap * 2 : 8; out = realloc(out, (size_t)out_cap * sizeof(Vec)); }
        out[out_len++] = (Vec){0, 0, NULL};
    }
    push(&out[h], t->v);
    return h;
}

int main(void) {
    enum { N = 400000 };
    static int64_t items[N]; static char present[N];
    vals = malloc(N * 8); lft = malloc(N * 8); rgt = malloc(N * 8);
    int64_t seed = 366, checksum = 0, groups = 0;
    for (int t = 0; t < 5; t++) {
        for (int64_t k = 0; k < N; k++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t r = seed / 65536;
            present[k] = !(k > 0 && r % 4 == 0);
            items[k] = r % 201 - 100;
        }
        links(items, present, N);
        out_len = 0;
        if (n_nodes > 0) { Tree *root = build(0); file_by_height(root); release(root); }
        for (int64_t g = 0; g < out_len; g++) {
            groups++;
            for (int64_t j = 0; j < out[g].len; j++) checksum = (checksum * 31 + out[g].a[j] + 101) % 1000000007;
            checksum = (checksum * 31 + 7) % 1000000007;
            free(out[g].a);
        }
    }
    printf("%lld groups, checksum %lld\n", (long long)groups, (long long)checksum);
    return 0;
}
