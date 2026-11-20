// LeetCode #1214 bench, in C: the ★ arm (each tree's values read in order,
// then two pointers, one climbing the first list and one coming down the
// second) on 16 pairs of balanced search trees of 5000 nodes each, built
// once; then 10 rounds over the pairs, four targets each, every answer
// folded into a checksum.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left, *right;
} TreeNode;

static long long seed = 1214;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long big(void) {
    long long hi = next_random();
    long long lo = next_random();
    return (hi * 32768 + lo) % 2000000001LL - 1000000000LL;
}

typedef struct {
    int *v;
    int n, cap;
} vec_t;

static void push(vec_t *v, int x) {
    if (v->n == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 16;
        v->v = realloc(v->v, v->cap * sizeof(int));
    }
    v->v[v->n++] = x;
}

static void in_order(TreeNode *node, vec_t *out) {
    if (!node) return;
    in_order(node->left, out);
    push(out, node->val);
    in_order(node->right, out);
}

static int two_sum_bsts(TreeNode *root1, TreeNode *root2, int target) {
    vec_t a = {0}, b = {0};
    in_order(root1, &a);
    in_order(root2, &b);
    int found = 0;
    long long i = 0, j = (long long)b.n - 1;
    while (i < a.n && j >= 0) {
        int sum = a.v[i] + b.v[j];
        if (sum == target) {
            found = 1;
            break;
        }
        if (sum < target) i++;
        else j--;
    }
    free(a.v);
    free(b.v);
    return found;
}

static TreeNode *balanced(const int *sorted, int low, int high) {
    if (low >= high) return NULL;
    int mid = (low + high) / 2;
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = sorted[mid];
    n->left = balanced(sorted, low, mid);
    n->right = balanced(sorted, mid + 1, high);
    return n;
}

/* n distinct values in increasing order: a sorted array, each new value
   put in its place by binary search, a value already there drawn again. */
static int *distinct_values(int n) {
    long long *s = malloc(n * sizeof(long long));
    int len = 0;
    while (len < n) {
        long long x = big();
        int lo = 0, hi = len;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (s[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        if (lo < len && s[lo] == x) continue;
        memmove(s + lo + 1, s + lo, (len - lo) * sizeof(long long));
        s[lo] = x;
        len++;
    }
    int *out = malloc(n * sizeof(int));
    for (int k = 0; k < n; k++) out[k] = (int)s[k];
    free(s);
    return out;
}

int main(void) {
    TreeNode *t1[16], *t2[16];
    int targets[16][4];
    for (int p = 0; p < 16; p++) {
        int *a = distinct_values(5000);
        int *b = distinct_values(5000);
        int i = (int)(next_random() % 5000);
        int j = (int)(next_random() % 5000);
        targets[p][0] = a[i] + b[j];
        targets[p][1] = a[j] + b[i];
        targets[p][2] = (int)big();
        targets[p][3] = (int)big();
        t1[p] = balanced(a, 0, 5000);
        t2[p] = balanced(b, 0, 5000);
        free(a);
        free(b);
    }
    long long check = 0;
    for (long long round = 0; round < 10; round++)
        for (int p = 0; p < 16; p++)
            for (int k = 0; k < 4; k++) {
                long long answer = two_sum_bsts(t1[p], t2[p], targets[p][k]) ? 2 : 1;
                check = (check * 131 + answer + round) % 1000000007LL;
            }
    printf("10 rounds over 16 pairs of 5000-node trees: checksum %lld\n", check);
    return 0;
}
