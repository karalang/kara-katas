// Benchmark harness for LeetCode #279 — Perfect Squares.
// Mirrors perfect_squares.kara algorithm-for-algorithm.

package main

import "fmt"

func numSquares(n int64) int64 {
	dp := make([]int64, 0)
	dp = append(dp, 0)
	for i := int64(1); i <= n; i++ {
		best := i
		for j := int64(1); j*j <= i; j++ {
			cand := dp[i-j*j] + 1
			if cand < best {
				best = cand
			}
		}
		dp = append(dp, best)
	}
	return dp[n]
}

func main() {
	const iters int64 = 100

	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		n := 25000 + (it*37)%5001
		sink = (sink*31 + numSquares(n)) % 1000000007
	}
	fmt.Println(sink)
}
