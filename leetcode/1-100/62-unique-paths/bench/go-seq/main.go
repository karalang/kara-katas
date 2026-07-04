// Benchmark workload — Unique Paths (LeetCode #62).
// Go single-threaded mirror of bench/unique_paths.{kara,rs,c}. Idiomatic Go:
// a GC-managed []int64 rolling-DP slice allocated per call, sized to the
// smaller axis. Same K/span sweep, the same dp[c] += dp[c-1] recurrence, and
// the same rolling polynomial-hash sink. See ../README.md § Benchmarks.

package main

import "fmt"

func uniquePaths(m, n int64) int64 {
	rows, cols := m, n
	if cols > rows {
		rows, cols = cols, rows
	}

	dp := make([]int64, cols)
	for j := range dp {
		dp[j] = 1
	}

	for i := int64(1); i < rows; i++ {
		for c := int64(1); c < cols; c++ {
			dp[c] = dp[c] + dp[c-1]
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
		ans := uniquePaths(m, n)
		acc = (acc*131 + ans) % modulus
	}
	fmt.Println(acc)
}
