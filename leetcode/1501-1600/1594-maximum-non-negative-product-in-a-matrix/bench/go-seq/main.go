// LeetCode #1594: Maximum Non Negative Product in a Matrix
// -- the bench in Go, mirroring product.kara: the largest and the
// smallest product of a path reaching each cell, in two [][]int64
// tables, on 40000 grids of 15 by 15 cells from -4 to 4, all drawn first.
package main

import (
	"fmt"
	"math"
)

var seed int64 = 1594

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maxProductPath(grid [][]int32) int32 {
	rows, cols := len(grid), len(grid[0])
	hi := make([][]int64, rows)
	lo := make([][]int64, rows)
	for r := range hi {
		hi[r] = make([]int64, cols)
		lo[r] = make([]int64, cols)
	}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			v := int64(grid[r][c])
			if r == 0 && c == 0 {
				hi[r][c], lo[r][c] = v, v
				continue
			}
			best, worst := int64(math.MinInt64), int64(math.MaxInt64)
			if r > 0 {
				best = max(best, hi[r-1][c]*v, lo[r-1][c]*v)
				worst = min(worst, hi[r-1][c]*v, lo[r-1][c]*v)
			}
			if c > 0 {
				best = max(best, hi[r][c-1]*v, lo[r][c-1]*v)
				worst = min(worst, hi[r][c-1]*v, lo[r][c-1]*v)
			}
			hi[r][c], lo[r][c] = best, worst
		}
	}
	top := hi[rows-1][cols-1]
	if top < 0 {
		return -1
	}
	return int32(top % 1000000007)
}

func main() {
	grids := make([][][]int32, 40000)
	for g := range grids {
		grids[g] = make([][]int32, 15)
		for r := range grids[g] {
			grids[g][r] = make([]int32, 15)
			for c := range grids[g][r] {
				grids[g][r][c] = int32(nextRandom()%9 - 4)
			}
		}
	}
	var check int64
	negative := 0
	for _, grid := range grids {
		answer := maxProductPath(grid)
		if answer == -1 {
			negative++
		}
		check = (check*31 + int64(answer) + 1) % 1000000007
	}
	fmt.Printf("40000 grids of 15 by 15: %d only negative, checksum %d\n", negative, check)
}
