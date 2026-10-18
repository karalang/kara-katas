// LeetCode #711: Number of Distinct Islands II -- canonical forms
// counted by sorting.
// Benchmark mirror of the Kara sorted arm: each island by depth-first
// search with a stack; its canonical form the smallest of its eight
// symmetries, sorted and moved to the origin; forms sorted and counted.
package main

import (
	"fmt"
	"slices"
)

type cell struct{ r, c int64 }

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func cmpCell(x, y cell) int {
	if x.r != y.r {
		if x.r < y.r {
			return -1
		}
		return 1
	}
	if x.c != y.c {
		if x.c < y.c {
			return -1
		}
		return 1
	}
	return 0
}

func canonical(cells []cell) []int64 {
	var best []int64
	for k := 0; k < 8; k++ {
		moved := make([]cell, 0, len(cells))
		for _, p := range cells {
			a, b := p.r, p.c
			if k >= 4 {
				a, b = p.c, p.r
			}
			if k%2 == 1 {
				a = -a
			}
			if k%4 >= 2 {
				b = -b
			}
			moved = append(moved, cell{a, b})
		}
		slices.SortFunc(moved, cmpCell)
		r0, c0 := moved[0].r, moved[0].c
		flat := make([]int64, 0, 2*len(moved))
		for _, p := range moved {
			flat = append(flat, p.r-r0, p.c-c0)
		}
		if k == 0 || slices.Compare(flat, best) < 0 {
			best = flat
		}
	}
	return best
}

func numDistinctIslands2(grid [][]int64) int64 {
	rows, cols := len(grid), len(grid[0])
	seen := make([]bool, rows*cols)
	var forms [][]int64
	for start := 0; start < rows*cols; start++ {
		if grid[start/cols][start%cols] == 0 || seen[start] {
			continue
		}
		var cells []cell
		stack := []int{start}
		seen[start] = true
		for len(stack) > 0 {
			at := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			r, c := at/cols, at%cols
			cells = append(cells, cell{int64(r), int64(c)})
			if r > 0 && grid[r-1][c] == 1 && !seen[at-cols] {
				seen[at-cols] = true
				stack = append(stack, at-cols)
			}
			if r+1 < rows && grid[r+1][c] == 1 && !seen[at+cols] {
				seen[at+cols] = true
				stack = append(stack, at+cols)
			}
			if c > 0 && grid[r][c-1] == 1 && !seen[at-1] {
				seen[at-1] = true
				stack = append(stack, at-1)
			}
			if c+1 < cols && grid[r][c+1] == 1 && !seen[at+1] {
				seen[at+1] = true
				stack = append(stack, at+1)
			}
		}
		forms = append(forms, canonical(cells))
	}
	slices.SortFunc(forms, slices.Compare[[]int64])
	count := int64(0)
	for i := range forms {
		if i == 0 || slices.Compare(forms[i], forms[i-1]) != 0 {
			count++
		}
	}
	return count
}

func main() {
	seed := int64(711)
	var grids [][][]int64
	for g := int64(0); g < 100; g++ {
		pct := 30 + g*2/5
		grid := make([][]int64, 50)
		for r := range grid {
			grid[r] = make([]int64, 50)
			for c := range grid[r] {
				if nextRandom(&seed)%100 < pct {
					grid[r][c] = 1
				}
			}
		}
		grids = append(grids, grid)
	}
	sum := int64(0)
	for round := 0; round < 10; round++ {
		for _, grid := range grids {
			sum += numDistinctIslands2(grid)
		}
	}
	fmt.Printf("10 rounds of 100 grids of 50 by 50: %d distinct islands\n", sum)
}
