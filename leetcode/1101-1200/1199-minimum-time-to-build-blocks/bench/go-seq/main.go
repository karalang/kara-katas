// LeetCode #1199 bench: the ★ arm in Go, over the same 200 sets of 1000
// blocks and 50 rounds as the Kāra bench; the smallest-first queue is
// `container/heap` over a copy of the blocks.
package main

import (
	"container/heap"
	"fmt"
)

type minHeap []int64

func (h minHeap) Len() int           { return len(h) }
func (h minHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x any)        { *h = append(*h, x.(int64)) }
func (h *minHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func minBuildTime(blocks []int64, split int64) int64 {
	h := make(minHeap, len(blocks))
	copy(h, blocks)
	heap.Init(&h)
	for h.Len() > 1 {
		heap.Pop(&h)
		slower := heap.Pop(&h).(int64)
		heap.Push(&h, slower+split)
	}
	return h[0]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	highs := []int64{10, 1000, 100000}
	seed := int64(1199)
	type set struct {
		blocks []int64
		split  int64
	}
	sets := make([]set, 0, 200)
	for k := 0; k < 200; k++ {
		high := highs[k%3]
		split := nextRandom(&seed)%100 + 1
		blocks := make([]int64, 1000)
		for j := range blocks {
			a := nextRandom(&seed)
			b := nextRandom(&seed)
			blocks[j] = (a*32768+b)%high + 1
		}
		sets = append(sets, set{blocks, split})
	}
	var check int64
	for r := 0; r < 50; r++ {
		for _, s := range sets {
			t := minBuildTime(s.blocks, s.split)
			check = (check*131 + t) % 1000000007
		}
	}
	fmt.Printf("50 rounds of 200 sets of 1000 blocks: checksum %d\n", check)
}
