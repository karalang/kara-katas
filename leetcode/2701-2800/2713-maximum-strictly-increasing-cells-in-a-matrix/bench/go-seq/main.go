// LeetCode #2713: Maximum Strictly Increasing Cells in a Matrix -- the
// bench (increasing.kara in Go): the cells sorted by value, each value's
// cells answered from their row's and column's best before any is
// recorded.
package main

import (
	"fmt"
	"sort"
)

type cell struct{ v, r, c int64 }

func maxIncreasingCells(mat [][]int64) int64 {
	m, n := len(mat), len(mat[0])
	cells := make([]cell, 0, m*n)
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			cells = append(cells, cell{mat[r][c], int64(r), int64(c)})
		}
	}
	sort.Slice(cells, func(a, b int) bool {
		x, y := cells[a], cells[b]
		if x.v != y.v {
			return x.v < y.v
		}
		if x.r != y.r {
			return x.r < y.r
		}
		return x.c < y.c
	})
	rowBest := make([]int64, m)
	colBest := make([]int64, n)
	found := make([]int64, 0)
	var best int64
	i := 0
	for i < len(cells) {
		j := i
		for j < len(cells) && cells[j].v == cells[i].v {
			j++
		}
		found = found[:0]
		for k := i; k < j; k++ {
			f := max(rowBest[cells[k].r], colBest[cells[k].c]) + 1
			found = append(found, f)
		}
		for k := i; k < j; k++ {
			r, c := cells[k].r, cells[k].c
			rowBest[r] = max(rowBest[r], found[k-i])
			colBest[c] = max(colBest[c], found[k-i])
			best = max(best, found[k-i])
		}
		i = j
	}
	return best
}

var seed int64 = 2713

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 10, 10
	mats := make([][][]int64, 0, count)
	for k := 0; k < count; k++ {
		spread := nextRandom()%9991 + 10
		mat := make([][]int64, 300)
		for r := range mat {
			mat[r] = make([]int64, 300)
			for c := range mat[r] {
				mat[r][c] = nextRandom() % spread
			}
		}
		mats = append(mats, mat)
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, mat := range mats {
			cells := maxIncreasingCells(mat)
			sum += cells
			check = (check*31 + cells + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d matrices of 300 by 300, %d rounds: cells sum to %d, checksum %d\n", count, rounds, sum, check)
}
