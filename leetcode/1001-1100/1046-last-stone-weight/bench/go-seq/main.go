// LeetCode #1046: Last Stone Weight -- benchmark driver, Go mirror of
// last_stone.kara, with container/heap as a largest-first queue.
package main

import (
	"container/heap"
	"fmt"
)

type maxHeap []int64

func (h maxHeap) Len() int            { return len(h) }
func (h maxHeap) Less(i, j int) bool  { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x interface{}) { *h = append(*h, x.(int64)) }
func (h *maxHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func lastStoneWeight(stones []int64) int64 {
	h := make(maxHeap, len(stones))
	copy(h, stones)
	heap.Init(&h)
	for {
		if h.Len() == 0 {
			return 0
		}
		y := heap.Pop(&h).(int64)
		if h.Len() == 0 {
			return y
		}
		x := heap.Pop(&h).(int64)
		if y > x {
			heap.Push(&h, y-x)
		}
	}
}

var seed int64 = 1046

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, rounds = 1000, 3000, 3
	piles := make([][]int64, count)
	for c := range piles {
		pile := make([]int64, n)
		for i := range pile {
			high := nextRandom()
			low := nextRandom()
			pile[i] = (high*32768+low)%1000000000 + 1
		}
		piles[c] = pile
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, pile := range piles {
			answer := lastStoneWeight(pile)
			total += answer
			check = (check*131 + answer%1000000007 + 1) % 1000000007
		}
	}
	fmt.Printf("%d piles of %d stones, %d rounds: total %d, checksum %d\n", count, n, rounds, total, check)
}
