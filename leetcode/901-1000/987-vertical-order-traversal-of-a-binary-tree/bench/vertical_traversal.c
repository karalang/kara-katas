// Benchmark: LeetCode #987 Vertical Order Traversal of a Binary Tree --
// the ★ arm, every node's place sorted, on random trees of 1000 nodes,
// LeetCode's largest. Mirrors vertical_traversal.kara, .rs, .py and
// go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct { int64_t col, row, val; } Place;

typedef struct { int64_t *items; int64_t len, cap; } Column;

typedef struct { Place *items; int64_t len, cap; } Places;

static void push_place(Places *p, Place x) {
    if (p->len == p->cap) {
        p->cap = p->cap ? p->cap * 2 : 4;
        p->items = realloc(p->items, sizeof(Place) * (size_t)p->cap);
    }
    p->items[p->len++] = x;
}

static void push_val(Column *c, int64_t v) {
    if (c->len == c->cap) {
        c->cap = c->cap ? c->cap * 2 : 4;
        c->items = realloc(c->items, sizeof(int64_t) * (size_t)c->cap);
    }
    c->items[c->len++] = v;
}

static void walk(TreeNode *t, int64_t row, int64_t col, Places *out) {
    if (t == NULL) return;
    push_place(out, (Place){col, row, t->val});
    walk(t->left, row + 1, col - 1, out);
    walk(t->right, row + 1, col + 1, out);
}

static int cmp_place(const void *x, const void *y) {
    const Place *a = x, *b = y;
    if (a->col != b->col) return a->col < b->col ? -1 : 1;
    if (a->row != b->row) return a->row < b->row ? -1 : 1;
    if (a->val != b->val) return a->val < b->val ? -1 : 1;
    return 0;
}

// The columns, each a growable list, in `*ncols`.
static Column *vertical_traversal(TreeNode *root, int64_t *ncols) {
    Places places = {0};
    walk(root, 0, 0, &places);
    qsort(places.items, (size_t)places.len, sizeof(Place), cmp_place);
    Column *out = NULL;
    int64_t len = 0, cap = 0, last = 0;
    for (int64_t i = 0; i < places.len; i++) {
        if (len == 0 || places.items[i].col != last) {
            if (len == cap) {
                cap = cap ? cap * 2 : 4;
                out = realloc(out, sizeof(Column) * (size_t)cap);
            }
            out[len++] = (Column){0};
            last = places.items[i].col;
        }
        push_val(&out[len - 1], places.items[i].val);
    }
    free(places.items);
    *ncols = len;
    return out;
}

static int64_t seed = 987;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(int64_t val) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = val;
    t->left = NULL;
    t->right = NULL;
    return t;
}

static TreeNode *random_tree(int n) {
    TreeNode *root = new_node(next_random() % 1001);
    for (int i = 1; i < n; i++) {
        TreeNode *node = new_node(next_random() % 1001), *cur = root;
        for (;;) {
            if (next_random() % 2 == 0) {
                if (cur->left) cur = cur->left;
                else { cur->left = node; break; }
            } else {
                if (cur->right) cur = cur->right;
                else { cur->right = node; break; }
            }
        }
    }
    return root;
}

int main(void) {
    int rounds = 500;
    TreeNode *trees[20];
    for (int i = 0; i < 20; i++) trees[i] = random_tree(1000);
    int64_t columns = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int64_t n;
            Column *cols = vertical_traversal(trees[(r + i) % 20], &n);
            columns += n;
            Column *mid = &cols[n / 2];
            check = (check * 31 + mid->len + mid->items[0]) % 1000000007;
            for (int64_t k = 0; k < n; k++) free(cols[k].items);
            free(cols);
        }
    }
    printf("%d rounds over 20 trees of 1000 nodes: %lld columns, checksum %lld\n", rounds,
           (long long)columns, (long long)check);
    return 0;
}
