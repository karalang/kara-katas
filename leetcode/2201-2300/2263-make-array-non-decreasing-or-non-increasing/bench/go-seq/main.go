// LeetCode #2263: Make Array Non-decreasing or Non-increasing -- Go
// mirror of the ★ arm (convert.kara): the slope trick on a max-first
// container/heap, forwards and over the reversed array, the smaller cost.
// Output is byte-identical to convert.kara.
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

func nondecreasingCost(nums []int64) int64 {
	h := &maxHeap{}
	var cost int64
	for _, x := range nums {
		heap.Push(h, x)
		if (*h)[0] > x {
			cost += heap.Pop(h).(int64) - x
			heap.Push(h, x)
		}
	}
	return cost
}

func convertArray(nums []int64) int64 {
	reversed := make([]int64, len(nums))
	for i, x := range nums {
		reversed[len(nums)-1-i] = x
	}
	up, down := nondecreasingCost(nums), nondecreasingCost(reversed)
	if up < down {
		return up
	}
	return down
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2263

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 400; t++ {
		nums := make([]int64, 1000)
		for i := range nums {
			nums[i] = nextRandom() % 1001
		}
		check = (check*31 + convertArray(nums)) % 1000000007
	}
	fmt.Printf("400 arrays of 1000: checksum %d\n", check)
}
