// Benchmark for #508: C mirror of the ★ arm (post-order with a count
// table); see find_frequent_tree_sum.kara. The count table is a fresh
// open-addressing hash table for every call, grown by doubling, as the
// ★ arm counts into `Map.new()`, and the answer a fresh array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int64_t *keys, *counts;
    uint8_t *used;
    int64_t len, cap;
} Table;

static uint64_t hash(int64_t k) {
    uint64_t x = (uint64_t)k;
    x ^= x >> 33;
    x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33;
    x *= 0xc4ceb9fe1a85ec53ULL;
    x ^= x >> 33;
    return x;
}

static void table_init(Table *t, int64_t cap) {
    t->cap = cap;
    t->len = 0;
    t->keys = malloc(cap * sizeof(int64_t));
    t->counts = malloc(cap * sizeof(int64_t));
    t->used = calloc(cap, 1);
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->counts);
    free(t->used);
}

static int64_t *slot(Table *t, int64_t k) {
    uint64_t i = hash(k) & (uint64_t)(t->cap - 1);
    while (t->used[i] && t->keys[i] != k) i = (i + 1) & (uint64_t)(t->cap - 1);
    if (!t->used[i]) {
        t->used[i] = 1;
        t->keys[i] = k;
        t->counts[i] = 0;
        t->len++;
    }
    return &t->counts[i];
}

static void count(Table *t, int64_t k) {
    if (2 * (t->len + 1) > t->cap) {
        Table bigger;
        table_init(&bigger, t->cap * 2);
        for (int64_t i = 0; i < t->cap; i++) {
            if (t->used[i]) *slot(&bigger, t->keys[i]) = t->counts[i];
        }
        table_free(t);
        *t = bigger;
    }
    *slot(t, k) += 1;
}

static int64_t subtree_sum(const TreeNode *n, Table *counts) {
    if (!n) return 0;
    int64_t sum = n->val + subtree_sum(n->left, counts) + subtree_sum(n->right, counts);
    count(counts, sum);
    return sum;
}

static int64_t *find_frequent_tree_sum(const TreeNode *root, int64_t *len) {
    Table counts;
    table_init(&counts, 16);
    subtree_sum(root, &counts);
    int64_t best = 0;
    for (int64_t i = 0; i < counts.cap; i++) {
        if (counts.used[i] && counts.counts[i] > best) best = counts.counts[i];
    }
    int64_t cap = 4, n = 0;
    int64_t *sums = malloc(cap * sizeof(int64_t));
    for (int64_t i = 0; i < counts.cap; i++) {
        if (counts.used[i] && counts.counts[i] == best) {
            if (n == cap) {
                cap *= 2;
                sums = realloc(sums, cap * sizeof(int64_t));
            }
            sums[n++] = counts.keys[i];
        }
    }
    table_free(&counts);
    *len = n;
    return sums;
}

// ---- benchmark --------------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *build(const int64_t *values, int64_t lo, int64_t hi, int64_t *seed) {
    if (lo >= hi) return NULL;
    int64_t mid = lo + next_random(seed) % (hi - lo);
    TreeNode *left = build(values, lo, mid, seed);
    TreeNode *right = build(values, mid + 1, hi, seed);
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = values[mid];
    n->left = left;
    n->right = right;
    return n;
}

int main(void) {
    // 100 random trees of 10,000 nodes, the values from -2 to 2, from -50
    // to 50, or from the whole range -100,000 to 100,000 in turn, built
    // once. Then each is solved 30 times.
    int64_t trees = 100;
    int64_t seed = 508;
    TreeNode **all = malloc(trees * sizeof(TreeNode *));
    int64_t *values = malloc(10000 * sizeof(int64_t));
    for (int64_t t = 0; t < trees; t++) {
        int64_t half = t % 3 == 0 ? 2 : t % 3 == 1 ? 50 : 100000;
        for (int64_t k = 0; k < 10000; k++) values[k] = next_random(&seed) % (2 * half + 1) - half;
        all[t] = build(values, 0, 10000, &seed);
    }
    int64_t found = 0, total = 0;
    for (int r = 0; r < 30; r++) {
        for (int64_t t = 0; t < trees; t++) {
            int64_t len;
            int64_t *sums = find_frequent_tree_sum(all[t], &len);
            for (int64_t i = 0; i < len; i++) {
                found++;
                total += sums[i];
            }
            free(sums);
        }
    }
    printf("%lld trees of 10000 nodes, 30 times each: %lld most frequent sums, adding up to %lld\n",
           (long long)trees, (long long)found, (long long)total);
    return 0;
}
