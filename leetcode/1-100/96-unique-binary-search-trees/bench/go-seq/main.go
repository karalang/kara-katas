// Benchmark workload for LeetCode #96 — Catalan DP-table, Go mirror.
// K reps of the O(n^2) DP at a data-dependent size (m = 2 + acc%18), folding each
// count into a rolling hash. A fresh slice per call, matching Kara's Vec.new.
package main

import "fmt"

const mod = 1000000007

func numTrees(n int64) int64 {
	dp := make([]int64, n+1)
	dp[0] = 1
	for k := int64(1); k <= n; k++ {
		var total int64 = 0
		for r := int64(1); r <= k; r++ {
			total += dp[r-1] * dp[k-r]
		}
		dp[k] = total
	}
	return dp[n]
}

func main() {
	var acc int64 = 1
	for rep := 0; rep < 5000000; rep++ {
		m := 2 + (acc % 18)
		c := numTrees(m)
		acc = (acc*1000003 + c) % mod
	}
	fmt.Printf("%d\n", acc)
}
