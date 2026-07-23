package main

import "fmt"

func maxI64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func minI64(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func calculateMinimumHP(grid []int64, dp []int64, m, n int64) int64 {
	for i := m - 1; i >= 0; i-- {
		base := i * n
		for j := n - 1; j >= 0; j-- {
			cell := grid[base+j]
			var need int64
			if i == m-1 && j == n-1 {
				need = maxI64(1, 1-cell)
			} else if i == m-1 {
				need = maxI64(1, dp[base+j+1]-cell)
			} else if j == n-1 {
				need = maxI64(1, dp[base+n+j]-cell)
			} else {
				ahead := minI64(dp[base+n+j], dp[base+j+1])
				need = maxI64(1, ahead-cell)
			}
			dp[base+j] = need
		}
	}
	return dp[0]
}

func main() {
	var m, n, passes int64 = 200, 200, 2000
	total := m * n
	grid := make([]int64, total)
	var state int64 = 12345
	for c := int64(0); c < total; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		grid[c] = (state % 121) - 100
	}
	dp := make([]int64, total)
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := (p*131 + 7) % total
		grid[idx] = -grid[idx]
		sink += calculateMinimumHP(grid, dp, m, n)
	}
	fmt.Println(sink)
}
