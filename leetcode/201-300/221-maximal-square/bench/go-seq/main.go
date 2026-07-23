package main

import "fmt"

func maxSide(grid []int64, dp []int64, rows, cols int64) int64 {
	for j := int64(0); j < cols; j++ {
		dp[j] = 0
	}
	var best int64 = 0
	for i := int64(0); i < rows; i++ {
		base := i * cols
		var prevDiag int64 = 0
		for j := int64(0); j < cols; j++ {
			temp := dp[j]
			if grid[base+j] == 1 {
				var v int64 = 1
				if i != 0 && j != 0 {
					m := dp[j]
					if dp[j-1] < m {
						m = dp[j-1]
					}
					if prevDiag < m {
						m = prevDiag
					}
					v = m + 1
				}
				dp[j] = v
				if v > best {
					best = v
				}
			} else {
				dp[j] = 0
			}
			prevDiag = temp
		}
	}
	return best
}

func main() {
	var rows, cols, passes int64 = 800, 800, 150
	total := rows * cols
	grid := make([]int64, total)
	var state int64 = 12345
	for c := int64(0); c < total; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		if state%100 < 62 {
			grid[c] = 1
		} else {
			grid[c] = 0
		}
	}
	dp := make([]int64, cols)
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := (p%rows)*cols + ((p*131+7)%cols)
		grid[idx] = 1 - grid[idx]
		sink += maxSide(grid, dp, rows, cols)
	}
	fmt.Println(sink)
}
