// Benchmark harness for LeetCode #264 — Ugly Number II.
// Mirrors ugly_number_ii.kara algorithm-for-algorithm.

package main

import "fmt"

func nthUgly(n int64) int64 {
	dp := make([]int64, 0)
	dp = append(dp, 1)

	i2, i3, i5 := 0, 0, 0

	for int64(len(dp)) < n {
		c2 := dp[i2] * 2
		c3 := dp[i3] * 3
		c5 := dp[i5] * 5

		next := c2
		if c3 < next {
			next = c3
		}
		if c5 < next {
			next = c5
		}

		dp = append(dp, next)

		if c2 == next {
			i2++
		}
		if c3 == next {
			i3++
		}
		if c5 == next {
			i5++
		}
	}
	return dp[n-1]
}

func main() {
	const iters int64 = 12000

	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		n := 9000 + (it*37)%3001
		sink = (sink*31 + nthUgly(n)) % 1000000007
	}
	fmt.Println(sink)
}
