// LeetCode #1254 bench, in Go: the ★ arm (each island flooded to water by
// recursion from its first cell, and counted when no cell of it reached
// the edge) on 100 random 100 by 100 grids built once, each with its own
// share of land from 20 to 80 in 100; each copied and asked 40 times,
// every count folded into a checksum.
package main

import "fmt"

var seed int64 = 1254

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func closed(grid [][]int64, i, j int) bool {
	if i < 0 || j < 0 || i >= len(grid) || j >= len(grid[0]) {
		return false
	}
	if grid[i][j] == 1 {
		return true
	}
	grid[i][j] = 1
	up := closed(grid, i-1, j)
	down := closed(grid, i+1, j)
	left := closed(grid, i, j-1)
	right := closed(grid, i, j+1)
	return up && down && left && right
}

func closedIsland(grid [][]int64) int64 {
	var count int64
	for i := range grid {
		for j := range grid[0] {
			if grid[i][j] == 0 && closed(grid, i, j) {
				count++
			}
		}
	}
	return count
}

func main() {
	grids := make([][][]int64, 0, 100)
	for g := 0; g < 100; g++ {
		land := nextRandom()%61 + 20
		grid := make([][]int64, 100)
		for i := range grid {
			grid[i] = make([]int64, 100)
			for j := range grid[i] {
				if nextRandom()%100 < land {
					grid[i][j] = 0
				} else {
					grid[i][j] = 1
				}
			}
		}
		grids = append(grids, grid)
	}
	var check int64
	for r := 0; r < 40; r++ {
		for _, grid := range grids {
			work := make([][]int64, len(grid))
			for i := range grid {
				work[i] = append([]int64(nil), grid[i]...)
			}
			check = (check*131 + closedIsland(work)) % 1000000007
		}
	}
	fmt.Printf("40 rounds of 100 grids of 100 by 100: checksum %d\n", check)
}
