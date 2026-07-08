// Benchmark workload — Minimum Path Sum (LeetCode #64).
// Go single-threaded mirror of bench/minimum_path_sum.{kara,rs,c}. Idiomatic Go:
// a GC-managed []int64 rolling-DP slice allocated per call, sized to the real
// column count n (costs break #62's axis symmetry — no swap). Same K/span sweep,
// the same dp[c] = cost + min(dp[c], dp[c-1]) recurrence, the same inline cost
// predicate ((i*7 + c*3 + k) % 13 + 1), and the same rolling polynomial-hash
// sink. See ../README.md § Benchmarks.

package main

import "fmt"

func imin(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func minPathSum(m, n, k int64) int64 {
	cols := n

	dp := make([]int64, cols)
	for j := int64(0); j < cols; j++ {
		cost := ((j*3 + k) % 13) + 1 // i == 0
		if j == 0 {
			dp[j] = cost
		} else {
			dp[j] = dp[j-1] + cost
		}
	}

	for i := int64(1); i < m; i++ {
		dp[0] = dp[0] + (((i*7 + k) % 13) + 1)
		for c := int64(1); c < cols; c++ {
			cost := ((i*7 + c*3 + k) % 13) + 1
			dp[c] = cost + imin(dp[c], dp[c-1])
		}
	}
	return dp[cols-1]
}

func main() {
	const total int64 = 1000000
	const modulus int64 = 1000000007
	const span int64 = 32

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		m := 2 + (k % span)
		n := 2 + ((k / span) % span)
		ans := minPathSum(m, n, k)
		acc = (acc*131 + ans) % modulus
	}
	fmt.Println(acc)
}
