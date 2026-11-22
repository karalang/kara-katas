// LeetCode #2850: Minimum Moves to Spread Stones Over Grid -- the
// bench: the ★ arm over every grid of nine stones, 24310 of them, all
// made first, then each answered 5 times.
package main

import (
	"fmt"
	"math"
)

type cell struct{ r, c int64 }

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func spread(k int, from, to []cell, used []bool) int64 {
	if k == len(from) {
		return 0
	}
	best := int64(math.MaxInt64)
	for j := range to {
		if !used[j] {
			used[j] = true
			d := abs(from[k].r-to[j].r) + abs(from[k].c-to[j].c) + spread(k+1, from, to, used)
			best = min(best, d)
			used[j] = false
		}
	}
	return best
}

func minimumMoves(grid [][]int64) int64 {
	from := []cell{}
	to := []cell{}
	for r := int64(0); r < 3; r++ {
		for c := int64(0); c < 3; c++ {
			if grid[r][c] == 0 {
				to = append(to, cell{r, c})
			}
			for i := int64(1); i < grid[r][c]; i++ {
				from = append(from, cell{r, c})
			}
		}
	}
	used := make([]bool, len(to))
	return spread(0, from, to, used)
}

func every(c int, left int64, counts []int64, out *[][][]int64) {
	if c == 8 {
		counts[8] = left
		grid := make([][]int64, 3)
		for r := 0; r < 3; r++ {
			grid[r] = []int64{counts[r*3], counts[r*3+1], counts[r*3+2]}
		}
		*out = append(*out, grid)
		return
	}
	for k := int64(0); k <= left; k++ {
		counts[c] = k
		every(c+1, left-k, counts, out)
	}
}

func main() {
	const rounds = 5
	counts := make([]int64, 9)
	grids := [][][]int64{}
	every(0, 9, counts, &grids)
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, grid := range grids {
			moves := minimumMoves(grid)
			total += moves
			check = (check*31 + moves + r) % 1000000007
		}
	}
	fmt.Printf("%d grids, %d rounds: %d moves, checksum %d\n", len(grids), rounds, total, check)
}
