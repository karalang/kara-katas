// Benchmark: LeetCode #1102 Path With Maximum Minimum Value -- a
// best-first search with a max-heap (container/heap) of (minimum, row,
// column), compared as tuples, as the Kāra ★ arm. Mirrors
// ../maximum_minimum_path.kara.
package main

import (
	"container/heap"
	"fmt"
)

type entry struct{ low, r, c int64 }

type maxHeap []entry

func (h maxHeap) Len() int { return len(h) }
func (h maxHeap) Less(i, j int) bool {
	a, b := h[i], h[j]
	if a.low != b.low {
		return a.low > b.low
	}
	if a.r != b.r {
		return a.r > b.r
	}
	return a.c > b.c
}
func (h maxHeap) Swap(i, j int)  { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x any)    { *h = append(*h, x.(entry)) }
func (h *maxHeap) Pop() any {
	old := *h
	e := old[len(old)-1]
	*h = old[:len(old)-1]
	return e
}

func maximumMinimumPath(grid [][]int64) int64 {
	m, n := int64(len(grid)), int64(len(grid[0]))
	done := make([][]bool, m)
	for i := range done {
		done[i] = make([]bool, n)
	}
	h := &maxHeap{{grid[0][0], 0, 0}}
	dirs := [4][2]int64{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	for h.Len() > 0 {
		e := heap.Pop(h).(entry)
		if done[e.r][e.c] {
			continue
		}
		done[e.r][e.c] = true
		if e.r == m-1 && e.c == n-1 {
			return e.low
		}
		for _, d := range dirs {
			nr, nc := e.r+d[0], e.c+d[1]
			if nr >= 0 && nr < m && nc >= 0 && nc < n && !done[nr][nc] {
				heap.Push(h, entry{min(e.low, grid[nr][nc]), nr, nc})
			}
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1102)
	grids := make([][][]int64, 32)
	for g := range grids {
		grids[g] = make([][]int64, 100)
		for r := range grids[g] {
			grids[g][r] = make([]int64, 100)
			for c := range grids[g][r] {
				grids[g][r][c] = nextRandom(&seed) * 30517 % 1000000000
			}
		}
	}
	var total, check int64
	for round := int64(0); round < 8; round++ {
		for j := int64(0); j < 32; j++ {
			at := (round*7919 + j*104729) % 10000
			grids[j][at/100][at%100] /= 2
			best := maximumMinimumPath(grids[j])
			total += best
			check = (check*31 + best%1000003 + 1) % 1000000007
		}
	}
	fmt.Printf("8 rounds over 32 grids of 100 by 100: minimums total %d, checksum %d\n", total, check)
}
