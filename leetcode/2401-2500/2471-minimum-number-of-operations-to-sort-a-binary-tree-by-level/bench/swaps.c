// LeetCode #2471: Minimum Number of Operations to Sort a Binary Tree by
// Level -- the bench, the ★ arm in C: the levels by a breadth-first walk,
// and in each the cycles of the permutation that sorts it. C has no hash
// map, so each value's sorted place is kept in an open-addressing table
// of 2^15 slots keyed by the value, its slots emptied again after every
// level. The nodes are one malloc'd array linked by pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

#define CAP (1 << 15)

typedef struct {
    int64_t key, value;
} Slot;

static Slot table[CAP];

static Slot *find(int64_t key) {
    uint64_t h = ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 49;
    while (table[h].key != 0 && table[h].key != key) h = (h + 1) & (CAP - 1);
    return &table[h];
}

static int cmp64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t minimum_operations(TreeNode *root, int64_t n) {
    TreeNode **level = malloc(sizeof(TreeNode *) * n);
    TreeNode **next = malloc(sizeof(TreeNode *) * n);
    int64_t *values = malloc(sizeof(int64_t) * n);
    int64_t *sorted = malloc(sizeof(int64_t) * n);
    char *seen = malloc(n);
    int64_t width = 0, total = 0;
    if (root) level[width++] = root;
    while (width > 0) {
        for (int64_t i = 0; i < width; i++) values[i] = level[i]->val;
        memcpy(sorted, values, sizeof(int64_t) * width);
        qsort(sorted, width, sizeof(int64_t), cmp64);
        for (int64_t i = 0; i < width; i++) {
            Slot *s = find(sorted[i]);
            s->key = sorted[i];
            s->value = i;
        }
        memset(seen, 0, width);
        for (int64_t i = 0; i < width; i++) {
            int64_t length = 0, at = i;
            while (!seen[at]) {
                seen[at] = 1;
                at = find(values[at])->value;
                length++;
            }
            if (length > 1) total += length - 1;
        }
        for (int64_t i = 0; i < width; i++) find(sorted[i])->key = 0;
        int64_t w = 0;
        for (int64_t i = 0; i < width; i++) {
            if (level[i]->left) next[w++] = level[i]->left;
            if (level[i]->right) next[w++] = level[i]->right;
        }
        TreeNode **t = level;
        level = next;
        next = t;
        width = w;
    }
    free(level);
    free(next);
    free(values);
    free(sorted);
    free(seen);
    return total;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2471;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

// the nodes of a random tree, the root first: the values 1 to `n` in a
// random order, each node after the first hung below a random earlier
// one, a random side taken down from it until a free one is found
static TreeNode *random_tree(int64_t n) {
    int64_t *values = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) values[i] = i + 1;
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = wide() % (i + 1);
        int64_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    TreeNode *nodes = malloc(sizeof(TreeNode) * n);
    for (int64_t i = 0; i < n; i++) {
        nodes[i].val = (int32_t)values[i];
        nodes[i].left = nodes[i].right = NULL;
    }
    for (int64_t k = 1; k < n; k++) {
        TreeNode *at = &nodes[wide() % k];
        for (;;) {
            if (next_random() % 2 == 0) {
                if (at->left) {
                    at = at->left;
                } else {
                    at->left = &nodes[k];
                    break;
                }
            } else {
                if (at->right) {
                    at = at->right;
                } else {
                    at->right = &nodes[k];
                    break;
                }
            }
        }
    }
    free(values);
    return nodes;
}

int main(void) {
    // 20 random trees of 10^4 nodes built once; then 110 passes, each
    // answering every tree, folding the count plus the pass into the
    // checksum, then swapping two of its values chosen by the checksum
    int64_t n = 10000;
    TreeNode *trees[20];
    for (int i = 0; i < 20; i++) trees[i] = random_tree(n);
    int64_t check = 0;
    for (int64_t p = 0; p < 110; p++) {
        for (int i = 0; i < 20; i++) {
            TreeNode *nodes = trees[i];
            check = (check * 31 + minimum_operations(&nodes[0], n) + p) % 1000000007;
            TreeNode *a = &nodes[check % n];
            TreeNode *b = &nodes[(check / n + p) % n];
            int32_t first = a->val;
            a->val = b->val;
            b->val = first;
        }
    }
    printf("110 passes over 20 trees of 10^4: checksum %lld\n", (long long)check);
    for (int i = 0; i < 20; i++) free(trees[i]);
    return 0;
}
