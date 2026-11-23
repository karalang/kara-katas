// LeetCode #2530: Maximal Score After Applying K Operations -- Go mirror of
// the benchmark (score.kara): the same numbers, passes, order and
// checksum, with container/heap over a max-ordered slice.
package main

import (
	"container/heap"
	"fmt"
)

type maxHeap []int64

func (h maxHeap) Len() int           { return len(h) }
func (h maxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x any)        { *h = append(*h, x.(int64)) }
func (h *maxHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func maxKelements(nums []int64, k int64) int64 {
	h := &maxHeap{}
	for _, x := range nums {
		heap.Push(h, x)
	}
	var score int64
	for s := int64(0); s < k; s++ {
		top := heap.Pop(h).(int64)
		score += top
		heap.Push(h, (top+2)/3)
	}
	return score
}

var seed int64 = 2530

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	nums := make([]int64, 100000)
	for i := range nums {
		nums[i] = wideRandom()%1000000000 + 1
	}
	const passes = 170
	var check int64
	for p := int64(0); p < passes; p++ {
		k := 50000 + check%50001
		check = (check*31 + maxKelements(nums, k)%1000000007 + p) % 1000000007
	}
	fmt.Printf("%d passes over 100000 numbers: checksum %d\n", passes, check)
}
