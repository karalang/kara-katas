// LeetCode #115 bench — distinct subsequences, Go mirror (2-D DP, [][]int64).
package main
import "fmt"
const MOD int64 = 1000000007
func numDistinct(s, t string) int64 {
    m, n := len(s), len(t)
    dp := make([][]int64, m+1)
    for i := range dp { dp[i] = make([]int64, n+1); dp[i][0] = 1 }
    for r := 1; r <= m; r++ {
        for c := 1; c <= n; c++ {
            skip := dp[r-1][c]
            if s[r-1] == t[c-1] { dp[r][c] = skip + dp[r-1][c-1] } else { dp[r][c] = skip }
        }
    }
    return dp[m][n]
}
func main() {
    ss := []string{"abcabcabcabcabcabcabcabc","aabbccaabbccaabbccaabbcc","abababababababababababab","xyzxyzxyzxyzxyzxyzxyzxyz","aaabbbcccaaabbbcccaaabbb","cbacbacbacbacbacbacbacba","abcabcabcabcabcabcabcabc","aabbaabbaabbaabbaabbaabb"}
    ts := []string{"abcabc","abcabc","ababa","xyzxy","abcab","cbacb","cba","abab"}
    var acc int64 = 1
    for rep := 0; rep < 400000; rep++ {
        idx := acc % 8
        c := numDistinct(ss[idx], ts[idx])
        acc = (acc*1000003 + c + 1) % MOD
    }
    fmt.Println(acc)
}
