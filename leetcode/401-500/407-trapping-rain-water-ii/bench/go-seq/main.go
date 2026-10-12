// Benchmark for #407: mirror of trapping_rain_water_ii.kara (a min-heap
// walking in from the border).
package main

import (
	"container/heap"
	"fmt"
)

type cell struct {
	level, r, c int64
}

type minHeap []cell

func (h minHeap) Len() int { return len(h) }
func (h minHeap) Less(i, j int) bool {
	if h[i].level != h[j].level {
		return h[i].level < h[j].level
	}
	if h[i].r != h[j].r {
		return h[i].r < h[j].r
	}
	return h[i].c < h[j].c
}
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(cell)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func trapRainWater(height [][]int64) int64 {
	m := int64(len(height))
	if m < 3 || len(height[0]) < 3 {
		return 0
	}
	n := int64(len(height[0]))
	seen := make([][]bool, m)
	for r := range seen {
		seen[r] = make([]bool, n)
	}
	h := &minHeap{}
	for r := int64(0); r < m; r++ {
		for c := int64(0); c < n; c++ {
			if r == 0 || c == 0 || r == m-1 || c == n-1 {
				heap.Push(h, cell{height[r][c], r, c})
				seen[r][c] = true
			}
		}
	}
	dr := [4]int64{1, -1, 0, 0}
	dc := [4]int64{0, 0, 1, -1}
	var water int64
	for h.Len() > 0 {
		top := heap.Pop(h).(cell)
		for d := 0; d < 4; d++ {
			nr := top.r + dr[d]
			nc := top.c + dc[d]
			if nr >= 0 && nr < m && nc >= 0 && nc < n && !seen[nr][nc] {
				seen[nr][nc] = true
				level := top.level
				if height[nr][nc] < level {
					water += level - height[nr][nc]
				} else {
					level = height[nr][nc]
				}
				heap.Push(h, cell{level, nr, nc})
			}
		}
	}
	return water
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	grids := 60
	size := 200
	var seed int64 = 407
	var total, checksum int64
	for g := 0; g < grids; g++ {
		grid := make([][]int64, size)
		for r := 0; r < size; r++ {
			grid[r] = make([]int64, size)
			for c := 0; c < size; c++ {
				hi := step(&seed)
				grid[r][c] = (hi*32768 + step(&seed)) % 20000
			}
		}
		w := trapRainWater(grid)
		total += w
		checksum = (checksum*31 + w) % 1000000007
	}
	fmt.Printf("%d grids of %d x %d: %d units of water, checksum %d\n", grids, size, size, total, checksum)
}
