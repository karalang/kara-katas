// Benchmark workload for LeetCode #97 — 2D interleaving-string DP, Go mirror.
package main

import "fmt"

const mod = 1000000007

func isInterleave(s1, s2, s3 string) bool {
	n, m := int64(len(s1)), int64(len(s2))
	if n+m != int64(len(s3)) {
		return false
	}
	stride := m + 1
	dp := make([]bool, (n+1)*stride)
	dp[0] = true
	for j := int64(1); j <= m; j++ {
		dp[j] = dp[j-1] && s2[j-1] == s3[j-1]
	}
	for i := int64(1); i <= n; i++ {
		dp[i*stride] = dp[(i-1)*stride] && s1[i-1] == s3[i-1]
		for j := int64(1); j <= m; j++ {
			up := dp[(i-1)*stride+j] && s1[i-1] == s3[i+j-1]
			left := dp[i*stride+j-1] && s2[j-1] == s3[i+j-1]
			dp[i*stride+j] = up || left
		}
	}
	return dp[n*stride+m]
}

func main() {
	s1s := []string{"baacccbabbacacabbbcabbcc", "abcababacbbacbcbccbcac", "abbaabbabacbcaaccbbcbcca", "bacaccbbaaacbaaaabaaaa", "cbabaabcacccbccaabbbc", "bacaacaccaccacabcbbcccb", "aaaccbbbcbaabbbcabbbbabc", "abbabbabcbcccaaacabbccbb", "caccbacaaacabbbcccb", "cccbacbaacbbbcbaaccbb", "aacbcaccaabbaababcccbc", "bbacbaabbabbaabccbacccaa"}
	s2s := []string{"baabaabbbcaccbcaaaaa", "cacccaaaccaaacccbcacabc", "bbacbacccccbaabccaacc", "ccbbaabcaacaccccbcccaca", "abaaabbbbccbaaccca", "babaaccaccbaaaacbcccc", "bbacaaaabaabbabacbcb", "ccbbabaaabaccababacacbbc", "bbccaabcbabcbcacacbccacc", "ccabccacabbbaabacbacb", "babcaabacabcbbcacab", "abbaacaabccbcaababbbbbc"}
	s3s := []string{"baabcaabcacabbbabbcaccbacabccaaaaaabbbcabbcc", "cabacccacbaaabaccacaaabbaccbccbcbccacbcacabcc", "bbaabbaabcbabcacbccaccbbcaaabacccaaccbbcbccca", "baccacccbbbaabaaabccabaacaccccbaacabaaaaccaca", "acbababaaabbbbcacbcbaacccabccccacaabbbc", "babbaacaaaccaccacccabccacabcabbcaccbaacbcccc", "aaabbacacaacabbbaabbbacbabacbcbabbbcabbbbabc", "cabbacbbbabbaaabaacbcbcacccabaaabacacbcbabcbccbb", "bcbacccacababcacbabcaabccaaacabbcbcccccbacc", "cccccbaabcbcacacacbabbbbcbbaabacbacbaaccbb", "aabcabbccaaacbaccabacabbbcbacaabababcccbc", "abbbbaaaccabaabcacbbbabcbaabaabbabbbcbcbaccccaa"}
	var acc int64 = 1
	for rep := 0; rep < 400000; rep++ {
		idx := acc % 12
		ok := isInterleave(s1s[idx], s2s[idx], s3s[idx])
		b := int64(0)
		if ok {
			b = 1
		}
		acc = (acc*131 + b + 1) % mod
	}
	fmt.Printf("%d\n", acc)
}
