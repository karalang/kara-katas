// LeetCode #115 bench — distinct subsequences, C mirror (2-D DP, nested long** table matching the
// Vec[Vec[i64]] / Vec<Vec<i64>> / [][]int64 the other mirrors use — apples-to-apples, not a flat
// contiguous array).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MOD 1000000007L
static long num_distinct(const char* s, const char* t) {
    long m = (long)strlen(s), n = (long)strlen(t);
    long** dp = malloc((size_t)(m+1)*sizeof(long*));
    for (long i=0;i<=m;i++) {
        dp[i] = malloc((size_t)(n+1)*sizeof(long));
        for (long j=0;j<=n;j++) dp[i][j] = (j==0)?1:0;
    }
    for (long r=1;r<=m;r++) for (long c=1;c<=n;c++) {
        long skip = dp[r-1][c];
        dp[r][c] = (s[r-1]==t[c-1]) ? skip + dp[r-1][c-1] : skip;
    }
    long res = dp[m][n];
    for (long i=0;i<=m;i++) free(dp[i]);
    free(dp);
    return res;
}
int main(void) {
    const char* ss[8] = {"abcabcabcabcabcabcabcabc","aabbccaabbccaabbccaabbcc","abababababababababababab","xyzxyzxyzxyzxyzxyzxyzxyz","aaabbbcccaaabbbcccaaabbb","cbacbacbacbacbacbacbacba","abcabcabcabcabcabcabcabc","aabbaabbaabbaabbaabbaabb"};
    const char* ts[8] = {"abcabc","abcabc","ababa","xyzxy","abcab","cbacb","cba","abab"};
    long acc = 1;
    for (long rep=0;rep<400000;rep++) {
        long idx = acc % 8;
        long c = num_distinct(ss[idx], ts[idx]);
        acc = (acc*1000003 + c + 1) % MOD;
    }
    printf("%ld\n", acc);
    return 0;
}
