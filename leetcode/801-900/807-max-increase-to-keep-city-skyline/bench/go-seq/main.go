// LeetCode 807 — Max Increase to Keep City Skyline: the bench.
//
// 64 grids of 50 by 50, LeetCode's largest, with heights from 0 to 100,
// are made once; each round finds how much the next one can grow.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func maxIncreaseKeepingSkyline(grid [][]int64) int64 {
	n := len(grid)
	rowMax := make([]int64, n)
	colMax := make([]int64, n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			rowMax[i] = max(rowMax[i], grid[i][j])
			colMax[j] = max(colMax[j], grid[i][j])
		}
	}
	var total int64
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			total += min(rowMax[i], colMax[j]) - grid[i][j]
		}
	}
	return total
}

func main() {
	seed := int64(807)
	grids := make([][][]int64, 0, 64)
	for g := 0; g < 64; g++ {
		grid := make([][]int64, 0, 50)
		for i := 0; i < 50; i++ {
			row := make([]int64, 50)
			for j := range row {
				row[j] = nextRandom(&seed) % 101
			}
			grid = append(grid, row)
		}
		grids = append(grids, grid)
	}
	rounds := int64(300000)
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		added := maxIncreaseKeepingSkyline(grids[r%64])
		total += added
		check = (check*131 + added) % 1000000007
	}
	fmt.Printf("%d rounds of 50 x 50: %d floors in all, checksum %d\n", rounds, total, check)
}
