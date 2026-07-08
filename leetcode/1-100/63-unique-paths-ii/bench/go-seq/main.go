// Benchmark workload — Unique Paths II (LeetCode #63).
// Go single-threaded mirror of bench/unique_paths_ii.{kara,rs,c}. Idiomatic Go:
// a GC-managed []int64 rolling-DP slice allocated per call, sized to the real
// column count n (obstacles break #62's axis symmetry — no swap). Same K/span
// sweep, the same dp[c] += dp[c-1] recurrence, the same inline obstacle
// predicate ((i*7 + c*3 + k) % 13 == 0), and the same rolling polynomial-hash
// sink. See ../README.md § Benchmarks.

package main

import "fmt"

func uniquePathsWithObstacles(m, n, k int64) int64 {
	cols := n

	dp := make([]int64, cols)
	dp[0] = 1

	for i := int64(0); i < m; i++ {
		for c := int64(0); c < cols; c++ {
			if (i*7+c*3+k)%13 == 0 {
				dp[c] = 0
			} else if c > 0 {
				dp[c] = dp[c] + dp[c-1]
			}
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
		ans := uniquePathsWithObstacles(m, n, k)
		acc = (acc*131 + ans) % modulus
	}
	fmt.Println(acc)
}
