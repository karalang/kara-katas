// LeetCode #1289 bench, in Go: the ★ arm (the row above's two smallest path
// sums) on 100 grids of 200 by 200, built once, 300 rounds, every answer
// folded into a checksum.
package main

import (
	"fmt"
	"math"
)

func minFallingPathSum(grid [][]int64) int64 {
	first, firstCol, second := int64(0), -1, int64(0)
	for _, row := range grid {
		nextFirst, nextCol, nextSecond := int64(math.MaxInt64), -1, int64(math.MaxInt64)
		for j, x := range row {
			prev := first
			if j == firstCol {
				prev = second
			}
			sum := x + prev
			if sum < nextFirst {
				nextSecond = nextFirst
				nextFirst = sum
				nextCol = j
			} else if sum < nextSecond {
				nextSecond = sum
			}
		}
		first, firstCol, second = nextFirst, nextCol, nextSecond
	}
	return first
}

var seed int64

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func problem(n int) [][]int64 {
	grid := make([][]int64, 0)
	for i := 0; i < n; i++ {
		row := make([]int64, 0)
		for j := 0; j < n; j++ {
			row = append(row, nextRandom()%199-99)
		}
		grid = append(grid, row)
	}
	return grid
}

func main() {
	seed = 1289
	grids := make([][][]int64, 0)
	for k := 0; k < 100; k++ {
		grids = append(grids, problem(200))
	}
	var check int64
	for round := int64(0); round < 300; round++ {
		for _, grid := range grids {
			check = (check*131 + minFallingPathSum(grid) + round + 1000000) % 1000000007
		}
	}
	fmt.Printf("300 rounds of 100 grids of 200 by 200: checksum %d\n", check)
}
