// Benchmark workload for LeetCode #113 — path sum II, C mirror (raw *Node + growable path list).
// Build 8 perfect depth-5 trees once, then K reps of backtracking path_sum collecting all 16
// root-to-leaf paths on a data-dependent-selected tree, folding the result into a rolling hash.
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007L
typedef struct Node { long val; struct Node *left, *right; } Node;
static Node* build_perfect(long depth, long val) {
    if (depth <= 0) return NULL;
    Node* n = malloc(sizeof(Node));
    n->val = val; n->left = build_perfect(depth-1,val); n->right = build_perfect(depth-1,val);
    return n;
}
typedef struct { long *vals; long len; } Path;
typedef struct { Path *items; long count, cap; } Paths;
static void paths_push(Paths *ps, long *path, long plen) {
    if (ps->count == ps->cap) { ps->cap = ps->cap ? ps->cap*2 : 8; ps->items = realloc(ps->items, ps->cap*sizeof(Path)); }
    long *copy = malloc(plen*sizeof(long));
    for (long i=0;i<plen;i++) copy[i]=path[i];
    ps->items[ps->count].vals = copy; ps->items[ps->count].len = plen; ps->count++;
}
static void dfs(Node* node, long target, long *path, long *plen, Paths *out) {
    if (!node) return;
    path[(*plen)++] = node->val;
    long rem = target - node->val;
    if (!node->left && !node->right) { if (rem == 0) paths_push(out, path, *plen); }
    else { dfs(node->left, rem, path, plen, out); dfs(node->right, rem, path, plen, out); }
    (*plen)--;
}
static void paths_free(Paths *ps){ for(long i=0;i<ps->count;i++) free(ps->items[i].vals); free(ps->items); }
static void free_tree(Node* n){ if(!n)return; free_tree(n->left); free_tree(n->right); free(n); }
int main(void) {
    Node* pool[8];
    for (long t=0;t<8;t++) pool[t]=build_perfect(5, t+1);
    long acc = 1, pathbuf[64];
    for (long rep=0; rep<300000; rep++) {
        long idx = acc % 8;
        Paths ps = {0}; long plen = 0;
        dfs(pool[idx], 5*(idx+1), pathbuf, &plen, &ps);
        long h = ps.count;
        for (long pi=0; pi<ps.count; pi++)
            for (long pj=0; pj<ps.items[pi].len; pj++)
                h = (h*131 + ps.items[pi].vals[pj]) % MOD;
        acc = (acc*1000003 + h + 1) % MOD;
        paths_free(&ps);
    }
    printf("%ld\n", acc);
    for (long t=0;t<8;t++) free_tree(pool[t]);
    return 0;
}
