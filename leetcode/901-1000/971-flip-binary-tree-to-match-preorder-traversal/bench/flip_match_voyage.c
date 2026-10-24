// Benchmark: LeetCode #971 Flip Binary Tree To Match Preorder Traversal
// -- the ★ arm, one walk flipping where the voyage says, on 200 random
// trees of 100 nodes. Mirrors flip_match_voyage.kara, .rs, .py and
// go-seq/. Each call mallocs its list of flips, as the other languages
// grow theirs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right;
} Node;

static Node *new_node(int64_t val) {
    Node *n = malloc(sizeof(Node));
    n->val = val;
    n->left = n->right = NULL;
    return n;
}

static int walk(const Node *t, const int64_t *voyage, int64_t *i, int64_t *flipped, int64_t *len) {
    if (t == NULL) return 1;
    if (t->val != voyage[*i]) return 0;
    (*i)++;
    if (t->left != NULL && t->left->val != voyage[*i]) {
        flipped[(*len)++] = t->val;
        return walk(t->right, voyage, i, flipped, len) && walk(t->left, voyage, i, flipped, len);
    }
    return walk(t->left, voyage, i, flipped, len) && walk(t->right, voyage, i, flipped, len);
}

// The flips in *out, their count returned; [-1] when none work.
static int64_t flip_match_voyage(const Node *root, const int64_t *voyage, int64_t n, int64_t **out) {
    int64_t *flipped = malloc(sizeof(int64_t) * (n + 1));
    int64_t i = 0, len = 0;
    if (!walk(root, voyage, &i, flipped, &len)) {
        flipped[0] = -1;
        len = 1;
    }
    *out = flipped;
    return len;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void random_permutation(int64_t *a, int64_t n, int64_t *seed) {
    for (int64_t v = 1; v <= n; v++) a[v - 1] = v;
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = next_random(seed) % (i + 1);
        int64_t t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
}

static Node *random_tree(const int64_t *vals, int64_t n, int64_t *seed) {
    Node *root = new_node(vals[0]);
    for (int64_t k = 1; k < n; k++) {
        Node *node = new_node(vals[k]);
        Node *cur = root;
        for (;;) {
            if (next_random(seed) % 2 == 0) {
                if (cur->left) {
                    cur = cur->left;
                } else {
                    cur->left = node;
                    break;
                }
            } else {
                if (cur->right) {
                    cur = cur->right;
                } else {
                    cur->right = node;
                    break;
                }
            }
        }
    }
    return root;
}

static void random_voyage(const Node *t, int64_t *seed, int64_t *out, int64_t *len) {
    if (t == NULL) return;
    out[(*len)++] = t->val;
    if (next_random(seed) % 2 == 0) {
        random_voyage(t->left, seed, out, len);
        random_voyage(t->right, seed, out, len);
    } else {
        random_voyage(t->right, seed, out, len);
        random_voyage(t->left, seed, out, len);
    }
}

int main(void) {
    const int64_t rounds = 1000, count = 200, n = 100;
    int64_t seed = 971;
    static Node *trees[200];
    static int64_t voyages[200][100];
    int64_t vals[100];
    for (int64_t c = 0; c < count; c++) {
        random_permutation(vals, n, &seed);
        trees[c] = random_tree(vals, n, &seed);
        int64_t len = 0;
        random_voyage(trees[c], &seed, voyages[c], &len);
        if (c % 4 == 3) {
            int64_t i = next_random(&seed) % n;
            int64_t j = next_random(&seed) % n;
            int64_t t = voyages[c][i];
            voyages[c][i] = voyages[c][j];
            voyages[c][j] = t;
        }
    }
    int64_t flips = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t s = 0; s < count; s++) {
            int64_t c = (r + s) % count;
            int64_t *got;
            int64_t len = flip_match_voyage(trees[c], voyages[c], n, &got);
            for (int64_t k = 0; k < len; k++) {
                flips++;
                check = (check * 31 + got[k] + 2) % 1000000007;
            }
            free(got);
        }
    }
    printf("%lld rounds over %lld trees of 100 nodes: %lld values, checksum %lld\n", (long long)rounds, (long long)count,
           (long long)flips, (long long)check);
    return 0;
}
