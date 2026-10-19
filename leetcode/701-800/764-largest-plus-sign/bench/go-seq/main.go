// LeetCode 764 — Largest Plus Sign: benchmark, the ★ arm in Go.
// 300 random grids of 500 x 500 with 5,000 mines each.
package main

import "fmt"

func orderOfLargestPlusSign(n int, mines [][]int) int64 {
	grid := make([][]int64, n)
	for i := range grid {
		grid[i] = make([]int64, n)
		for j := range grid[i] {
			grid[i][j] = int64(n)
		}
	}
	for _, mine := range mines {
		grid[mine[0]][mine[1]] = 0
	}
	for i := 0; i < n; i++ {
		var left, right, up, down int64
		for j := 0; j < n; j++ {
			if grid[i][j] == 0 {
				left = 0
			} else {
				left++
			}
			grid[i][j] = min(grid[i][j], left)
			k := n - 1 - j
			if grid[i][k] == 0 {
				right = 0
			} else {
				right++
			}
			grid[i][k] = min(grid[i][k], right)
			if grid[j][i] == 0 {
				up = 0
			} else {
				up++
			}
			grid[j][i] = min(grid[j][i], up)
			if grid[k][i] == 0 {
				down = 0
			} else {
				down++
			}
			grid[k][i] = min(grid[k][i], down)
		}
	}
	var best int64
	for _, row := range grid {
		for _, order := range row {
			best = max(best, order)
		}
	}
	return best
}

var seed int64 = 764

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, n := 300, 500
	var total, check int64
	for r := 0; r < rounds; r++ {
		taken := make([]bool, n*n)
		var mines [][]int
		for len(mines) < 5000 {
			row := int(nextRandom() % int64(n))
			col := int(nextRandom() % int64(n))
			if !taken[row*n+col] {
				taken[row*n+col] = true
				mines = append(mines, []int{row, col})
			}
		}
		order := orderOfLargestPlusSign(n, mines)
		total += order
		check = (check*31 + order) % 1000000007
	}
	fmt.Printf("%d grids of 500 x 500 with 5000 mines: orders adding up to %d, checksum %d\n", rounds, total, check)
}
