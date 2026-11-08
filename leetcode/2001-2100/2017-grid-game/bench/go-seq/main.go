// LeetCode #2017: Grid Game -- the ★ arm's benchmark, a mirror of grid.kara.
package main

import (
	"fmt"
	"math"
)

func gridGame(grid [][]int64) int64 {
	var top, bottom int64
	for _, v := range grid[0] {
		top += v
	}
	best := int64(math.MaxInt64)
	for i := range grid[0] {
		top -= grid[0][i]
		share := top
		if bottom > share {
			share = bottom
		}
		if share < best {
			best = share
		}
		bottom += grid[1][i]
	}
	return best
}

var seed int64 = 2017

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int64, 0, 200)
	for g := 0; g < 200; g++ {
		grid := make([][]int64, 2)
		for r := 0; r < 2; r++ {
			row := make([]int64, 50000)
			for c := range row {
				row[c] = nextRandom()*3%100000 + 1
			}
			grid[r] = row
		}
		grids = append(grids, grid)
	}
	var calls, sum, check int64
	for r := 0; r < 10; r++ {
		for _, grid := range grids {
			answer := gridGame(grid)
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
