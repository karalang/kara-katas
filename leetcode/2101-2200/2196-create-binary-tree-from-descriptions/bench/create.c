// benchmark's C mirror of create.kara (LeetCode #2196, the ★ arm): a hash
// map of nodes made as named, a hash set of children, both open
// addressing; each node malloc'd, and the tree freed after it is weighed.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    long long val;
    struct TreeNode *left, *right;
} TreeNode;

#define CAP 32768 /* a power of two above twice the 10^4 + 1 values */

typedef struct {
    long long key[CAP];
    TreeNode *node[CAP];
    char used[CAP];
} Map;

typedef struct {
    long long key[CAP];
    char used[CAP];
} Set;

static unsigned slot_of(long long v) {
    unsigned long long h = (unsigned long long)v * 0x9E3779B97F4A7C15ULL;
    return (unsigned)(h >> 49) & (CAP - 1);
}

static TreeNode *map_get(Map *m, long long v) {
    for (unsigned i = slot_of(v);; i = (i + 1) & (CAP - 1)) {
        if (!m->used[i]) return NULL;
        if (m->key[i] == v) return m->node[i];
    }
}

static void map_put(Map *m, long long v, TreeNode *n) {
    unsigned i = slot_of(v);
    while (m->used[i] && m->key[i] != v) i = (i + 1) & (CAP - 1);
    m->used[i] = 1;
    m->key[i] = v;
    m->node[i] = n;
}

static void set_add(Set *s, long long v) {
    unsigned i = slot_of(v);
    while (s->used[i] && s->key[i] != v) i = (i + 1) & (CAP - 1);
    s->used[i] = 1;
    s->key[i] = v;
}

static int set_has(Set *s, long long v) {
    for (unsigned i = slot_of(v);; i = (i + 1) & (CAP - 1)) {
        if (!s->used[i]) return 0;
        if (s->key[i] == v) return 1;
    }
}

static TreeNode *node_of(Map *m, long long v) {
    TreeNode *n = map_get(m, v);
    if (n) return n;
    n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = n->right = NULL;
    map_put(m, v, n);
    return n;
}

static Map nodes;
static Set children;

static TreeNode *create_binary_tree(long long (*d)[3], int len) {
    memset(nodes.used, 0, sizeof nodes.used);
    memset(children.used, 0, sizeof children.used);
    for (int i = 0; i < len; i++) {
        TreeNode *parent = node_of(&nodes, d[i][0]);
        TreeNode *child = node_of(&nodes, d[i][1]);
        if (d[i][2] == 1) parent->left = child;
        else parent->right = child;
        set_add(&children, d[i][1]);
    }
    for (int i = 0; i < len; i++)
        if (!set_has(&children, d[i][0])) return map_get(&nodes, d[i][0]);
    return NULL;
}

static long long seed = 2196;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long wide_random(void) {
    long long a = next_random();
    return a * 32768 + next_random();
}

#define N 10001

static void random_descriptions(long long (*d)[3]) {
    static long long values[100000];
    static long long free_p[2 * N + 2], free_side[2 * N + 2];
    for (int i = 0; i < 100000; i++) values[i] = i + 1;
    for (int i = 0; i < N; i++) {
        int j = i + (int)(wide_random() % (100000 - i));
        long long t = values[i]; values[i] = values[j]; values[j] = t;
    }
    int nfree = 2;
    free_p[0] = 0; free_side[0] = 1;
    free_p[1] = 0; free_side[1] = 0;
    for (int k = 1; k < N; k++) {
        int pick = (int)(wide_random() % nfree);
        long long p = free_p[pick], side = free_side[pick];
        nfree--;
        free_p[pick] = free_p[nfree];
        free_side[pick] = free_side[nfree];
        d[k - 1][0] = values[p]; d[k - 1][1] = values[k]; d[k - 1][2] = side;
        free_p[nfree] = k; free_side[nfree] = 1; nfree++;
        free_p[nfree] = k; free_side[nfree] = 0; nfree++;
    }
    for (int i = N - 2; i > 0; i--) {
        int j = (int)(wide_random() % (i + 1));
        for (int c = 0; c < 3; c++) {
            long long t = d[i][c]; d[i][c] = d[j][c]; d[j][c] = t;
        }
    }
}

static TreeNode *stack_n[N];
static long long stack_d[N];

static void weigh(TreeNode *root, long long *count, long long *weight) {
    int top = 0;
    *count = 0;
    *weight = 0;
    if (root) { stack_n[top] = root; stack_d[top] = 1; top++; }
    while (top > 0) {
        top--;
        TreeNode *n = stack_n[top];
        long long depth = stack_d[top];
        (*count)++;
        *weight += n->val * depth;
        if (n->left) { stack_n[top] = n->left; stack_d[top] = depth + 1; top++; }
        if (n->right) { stack_n[top] = n->right; stack_d[top] = depth + 1; top++; }
        free(n);
    }
}

int main(void) {
    static long long sets[20][N - 1][3];
    for (int s = 0; s < 20; s++) random_descriptions(sets[s]);
    long long check = 0;
    for (int pass = 0; pass < 50; pass++) {
        for (int s = 0; s < 20; s++) {
            long long count, weight;
            weigh(create_binary_tree(sets[s], N - 1), &count, &weight);
            check = (check * 31 + count + weight % 1000000007) % 1000000007;
        }
    }
    printf("50 passes over 20 trees: checksum %lld\n", check);
    return 0;
}
