// Benchmark workload for LeetCode #97 — 2D interleaving-string DP, C mirror.
// K reps of the O(|s1|*|s2|) DP at a data-dependent case (idx=acc%12), folding each
// verdict into a rolling hash. malloc/free a fresh bool table per call.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007LL

static int is_interleave(const char *s1, const char *s2, const char *s3) {
    long long n = (long long)strlen(s1), m = (long long)strlen(s2);
    if (n + m != (long long)strlen(s3)) return 0;
    long long stride = m + 1;
    char *dp = calloc((size_t)((n + 1) * stride), 1);
    dp[0] = 1;
    for (long long j = 1; j <= m; j++) dp[j] = dp[j - 1] && (s2[j - 1] == s3[j - 1]);
    for (long long i = 1; i <= n; i++) {
        dp[i * stride] = dp[(i - 1) * stride] && (s1[i - 1] == s3[i - 1]);
        for (long long j = 1; j <= m; j++) {
            int up = dp[(i - 1) * stride + j] && (s1[i - 1] == s3[i + j - 1]);
            int left = dp[i * stride + j - 1] && (s2[j - 1] == s3[i + j - 1]);
            dp[i * stride + j] = up || left;
        }
    }
    int res = dp[n * stride + m];
    free(dp);
    return res;
}

int main(void) {
    const char *s1s[] = {"baacccbabbacacabbbcabbcc", "abcababacbbacbcbccbcac", "abbaabbabacbcaaccbbcbcca", "bacaccbbaaacbaaaabaaaa", "cbabaabcacccbccaabbbc", "bacaacaccaccacabcbbcccb", "aaaccbbbcbaabbbcabbbbabc", "abbabbabcbcccaaacabbccbb", "caccbacaaacabbbcccb", "cccbacbaacbbbcbaaccbb", "aacbcaccaabbaababcccbc", "bbacbaabbabbaabccbacccaa"};
    const char *s2s[] = {"baabaabbbcaccbcaaaaa", "cacccaaaccaaacccbcacabc", "bbacbacccccbaabccaacc", "ccbbaabcaacaccccbcccaca", "abaaabbbbccbaaccca", "babaaccaccbaaaacbcccc", "bbacaaaabaabbabacbcb", "ccbbabaaabaccababacacbbc", "bbccaabcbabcbcacacbccacc", "ccabccacabbbaabacbacb", "babcaabacabcbbcacab", "abbaacaabccbcaababbbbbc"};
    const char *s3s[] = {"baabcaabcacabbbabbcaccbacabccaaaaaabbbcabbcc", "cabacccacbaaabaccacaaabbaccbccbcbccacbcacabcc", "bbaabbaabcbabcacbccaccbbcaaabacccaaccbbcbccca", "baccacccbbbaabaaabccabaacaccccbaacabaaaaccaca", "acbababaaabbbbcacbcbaacccabccccacaabbbc", "babbaacaaaccaccacccabccacabcabbcaccbaacbcccc", "aaabbacacaacabbbaabbbacbabacbcbabbbcabbbbabc", "cabbacbbbabbaaabaacbcbcacccabaaabacacbcbabcbccbb", "bcbacccacababcacbabcaabccaaacabbcbcccccbacc", "cccccbaabcbcacacacbabbbbcbbaabacbacbaaccbb", "aabcabbccaaacbaccabacabbbcbacaabababcccbc", "abbbbaaaccabaabcacbbbabcbaabaabbabbbcbcbaccccaa"};
    long long acc = 1;
    for (long long rep = 0; rep < 400000; rep++) {
        long long idx = acc % 12;
        int ok = is_interleave(s1s[idx], s2s[idx], s3s[idx]);
        acc = (acc * 131 + (ok ? 1 : 0) + 1) % MOD;
    }
    printf("%lld\n", acc);
    return 0;
}
