// Benchmark workload for LeetCode #112 — path sum, C mirror (*Node, read-only).
// Build 8 balanced 31-node trees once, then K reps of has_path_sum against an unachievable
// target (full traversal) on a data-dependent-selected tree, folding each verdict.
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007LL
typedef struct Node { long long val; struct Node *left, *right; } Node;
static Node* build(long long lo,long long hi){ if(lo>hi) return NULL; long long m=(lo+hi)/2; Node*n=malloc(sizeof(Node)); n->val=m; n->left=build(lo,m-1); n->right=build(m+1,hi); return n; }
static int has_path_sum(Node* n,long long target){
    if(!n) return 0;
    long long rem=target-n->val;
    if(!n->left && !n->right) return rem==0;
    return has_path_sum(n->left,rem) || has_path_sum(n->right,rem);
}
static void free_tree(Node* n){ if(!n) return; free_tree(n->left); free_tree(n->right); free(n); }
int main(void){
    Node* pool[8];
    for(long long t=0;t<8;t++) pool[t]=build(t*100,t*100+30);
    long long acc=1;
    for(long long rep=0;rep<6000000;rep++){
        long long idx=acc%8;
        int hit=has_path_sum(pool[idx],1000000000LL);
        acc=(acc*131 + (hit?1:0) + 1)%MOD;
    }
    printf("%lld\n",acc);
    for(long long t=0;t<8;t++) free_tree(pool[t]);
    return 0;
}
