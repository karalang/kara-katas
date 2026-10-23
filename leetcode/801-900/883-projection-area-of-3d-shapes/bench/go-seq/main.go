// LeetCode #883 bench: Go mirror of projection_area.kara (the ★ arm, one
// pass over rows and columns together) on the same 100 grids.
package main

import "fmt"

func projectionArea(grid [][]int64) int64 {
	n := len(grid)
	var area int64
	for i := 0; i < n; i++ {
		var row, column int64
		for j := 0; j < n; j++ {
			if grid[i][j] > 0 {
				area++
			}
			row = max(row, grid[i][j])
			column = max(column, grid[j][i])
		}
		area += row + column
	}
	return area
}

var seed int64 = 883

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var total, check int64
	for g := 0; g < 100; g++ {
		// a grid of 40 x 40 to 50 x 50, towers up to 50, a quarter empty
		n := 40 + nextRandom()%11
		grid := make([][]int64, n)
		for i := range grid {
			grid[i] = make([]int64, n)
			for j := range grid[i] {
				if nextRandom()%4 == 0 {
					grid[i][j] = 0
				} else {
					grid[i][j] = nextRandom() % 51
				}
			}
		}
		// 1000 towers rebuilt one at a time, the area after each
		for k := 0; k < 1000; k++ {
			i := nextRandom() % n
			j := nextRandom() % n
			grid[i][j] = nextRandom() % 51
			area := projectionArea(grid)
			total += area
			check = (check*131 + area) % 1000000007
		}
	}
	fmt.Printf("100 grids, 1000 towers rebuilt in each: area %d, checksum %d\n", total, check)
}
