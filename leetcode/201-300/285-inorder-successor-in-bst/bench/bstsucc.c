/* LeetCode 285 bench mirror — C. Same flat-arena BST, same descent, same
 * Option-folding sink (absent collapses to -1 inside the hash). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 300000
#define QUERIES 2000000
static int64_t *key, *lft, *rgt; static int64_t cnt;
static void bst_insert(int64_t k) {
    if (cnt == 0) { key[0]=k; lft[0]=-1; rgt[0]=-1; cnt=1; return; }
    int64_t cur = 0;
    for (;;) {
        if (k < key[cur]) {
            if (lft[cur] < 0) { key[cnt]=k; lft[cnt]=-1; rgt[cnt]=-1; lft[cur]=cnt; cnt++; return; }
            cur = lft[cur];
        } else {
            if (rgt[cur] < 0) { key[cnt]=k; lft[cnt]=-1; rgt[cnt]=-1; rgt[cur]=cnt; cnt++; return; }
            cur = rgt[cur];
        }
    }
}
/* returns 1 and sets *out when a successor exists, 0 otherwise */
static int successor(int64_t target, int64_t *out) {
    if (cnt == 0) return 0;
    int64_t cur = 0; int have = 0; int64_t best = 0;
    while (cur >= 0) {
        if (key[cur] > target) { best = key[cur]; have = 1; cur = lft[cur]; }
        else cur = rgt[cur];
    }
    if (have) *out = best;
    return have;
}
int main(void) {
    key = malloc((size_t)N*sizeof(int64_t)); lft = malloc((size_t)N*sizeof(int64_t)); rgt = malloc((size_t)N*sizeof(int64_t));
    int64_t seed = 20260825;
    for (int64_t i = 0; i < N; i++) { seed = (seed*1103515245LL+12345LL)%2147483648LL; bst_insert(seed % 1000000LL); }
    int64_t sink = 0, found = 0;
    for (int64_t q = 0; q < QUERIES; q++) {
        seed = (seed*1103515245LL+12345LL)%2147483648LL;
        int64_t target = seed % 1000000LL, v = 0;
        int have = successor(target, &v);
        if (have) found++;
        sink = (sink*31 + (have ? v : -1)) % 1000000007LL;
    }
    printf("%lld %lld\n", (long long)sink, (long long)found);
    return 0;
}
