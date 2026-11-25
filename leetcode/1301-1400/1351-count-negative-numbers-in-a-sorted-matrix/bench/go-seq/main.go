// LeetCode #1351 bench -- Go: a staircase walk from the bottom-left corner.
package main

import "fmt"

func countNegatives(grid [][]int32) int {
	n := len(grid[0])
	row, col, count := len(grid)-1, 0, 0
	for row >= 0 && col < n {
		if grid[row][col] < 0 {
			count += n - col
			row--
		} else {
			col++
		}
	}
	return count
}

func main() {
	var seed int64 = 1351
	grids := make([][][]int32, 50)
	for k := range grids {
		grid := make([][]int32, 100)
		for i := range grid {
			grid[i] = make([]int32, 100)
			for j := range grid[i] {
				v := int32(60)
				if i > 0 && grid[i-1][j] < v {
					v = grid[i-1][j]
				}
				if j > 0 && grid[i][j-1] < v {
					v = grid[i][j-1]
				}
				if i+j > 0 {
					seed = (seed*1103515245 + 12345) % 2147483648
					v -= int32((seed / 65536) % 2)
				}
				if v < -100 {
					v = -100
				}
				grid[i][j] = v
			}
		}
		grids[k] = grid
	}
	var check int64
	for r := int64(0); r < 300000; r++ {
		k, i, j := check%50, (check/50)%100, (check/5000)%100
		g := grids[k]
		var v int32
		if check%2 == 0 {
			v = 100
			if i > 0 && g[i-1][j] < v {
				v = g[i-1][j]
			}
			if j > 0 && g[i][j-1] < v {
				v = g[i][j-1]
			}
		} else {
			v = -100
			if i < 99 && g[i+1][j] > v {
				v = g[i+1][j]
			}
			if j < 99 && g[i][j+1] > v {
				v = g[i][j+1]
			}
		}
		g[i][j] = v
		check = (check*31 + int64(countNegatives(g)) + r) % 1000000007
	}
	fmt.Printf("300000 rounds over 50 grids of 100 by 100: checksum %d\n", check)
}
