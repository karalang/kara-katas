// LeetCode #1167: Minimum Cost to Connect Sticks -- the ★ arm's bench in
// Go: container/heap over a slice, built with heap.Init, the two shortest
// joined and the join pushed back.
package main

import (
	"container/heap"
	"fmt"
)

type minHeap []int64

func (h minHeap) Len() int            { return len(h) }
func (h minHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(int64)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func connectSticks(sticks []int64) int64 {
	h := make(minHeap, len(sticks))
	copy(h, sticks)
	heap.Init(&h)
	var cost int64
	for h.Len() > 1 {
		a := heap.Pop(&h).(int64)
		b := heap.Pop(&h).(int64)
		cost += a + b
		heap.Push(&h, a+b)
	}
	return cost
}

var seed int64 = 1167

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	piles := make([][]int64, 16)
	for k := range piles {
		piles[k] = make([]int64, 10000)
		for i := range piles[k] {
			piles[k][i] = 1 + nextRandom()%10000
		}
	}
	var total, check int64
	for r := 0; r < 40; r++ {
		for k := 0; k < 16; k++ {
			at := nextRandom() % 10000
			piles[k][at] = 1 + nextRandom()%10000
			c := connectSticks(piles[k])
			total += c
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("40 rounds over 16 piles of 10^4 sticks: total %d, checksum %d\n", total, check)
}
