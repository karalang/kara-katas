// LeetCode #120 — Go mirror, bottom-up rolling min-path DP.
// Same algorithm + workload as triangle.kara: build one N-row triangle once, then punch the O(N^2)
// min-path DP K=20000 times with a data-dependent seed (base-row perturbation (seed+j)%7). GC data point.
package main

import "fmt"

const MOD int64 = 1000000007

func minPath(tri [][]int64, seed int64) int64 {
	n := int64(len(tri))
	dp := make([]int64, n)
	for j := int64(0); j < n; j++ {
		dp[j] = tri[n-1][j] + ((seed + j) % 7)
	}
	for i := n - 2; i >= 0; i-- {
		for k := int64(0); k <= i; k++ {
			a, b := dp[k], dp[k+1]
			m := a
			if b < a {
				m = b
			}
			dp[k] = tri[i][k] + m
		}
	}
	return dp[0]
}

func main() {
	var nrows int64 = 200
	tri := make([][]int64, nrows)
	for i := int64(0); i < nrows; i++ {
		tri[i] = make([]int64, i+1)
		for j := int64(0); j <= i; j++ {
			tri[i][j] = (i*31 + j*17) % 100
		}
	}
	var acc int64 = 0
	for rep := 0; rep < 20000; rep++ {
		seed := acc % 97
		mp := minPath(tri, seed)
		acc = (acc*131 + mp) % MOD
	}
	fmt.Println(acc)
}
