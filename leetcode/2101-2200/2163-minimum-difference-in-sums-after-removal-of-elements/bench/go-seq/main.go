// LeetCode #2163: Minimum Difference in Sums After Removal of Elements --
// the benchmark's Go mirror of difference.kara: container/heap, one heap
// type for each order.
package main

import (
	"container/heap"
	"fmt"
	"math"
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

type minHeap []int64

func (h minHeap) Len() int            { return len(h) }
func (h minHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(int64)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func minimumDifference(nums []int64) int64 {
	n := len(nums) / 3
	kept := &maxHeap{}
	var sum int64
	left := make([]int64, 0, n+1)
	for i := 0; i < 2*n; i++ {
		heap.Push(kept, nums[i])
		sum += nums[i]
		if kept.Len() > n {
			sum -= heap.Pop(kept).(int64)
		}
		if i >= n-1 {
			left = append(left, sum)
		}
	}
	low := &minHeap{}
	sum = 0
	best := int64(math.MaxInt64)
	for i := 3*n - 1; i >= n; i-- {
		heap.Push(low, nums[i])
		sum += nums[i]
		if low.Len() > n {
			sum -= heap.Pop(low).(int64)
		}
		if i <= 2*n && left[i-n]-sum < best {
			best = left[i-n] - sum
		}
	}
	return best
}

var seed int64 = 2163

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	lists := make([][]int64, 4)
	for k := range lists {
		lists[k] = make([]int64, 300000)
		for i := range lists[k] {
			lists[k][i] = wideRandom()%100000 + 1
		}
	}
	var check int64
	for r := 0; r < 5; r++ {
		for k := 0; k < 4; k++ {
			at := wideRandom() % 300000
			lists[k][at] = wideRandom()%100000 + 1
			cp := append([]int64(nil), lists[k]...)
			d := minimumDifference(cp)
			check = (check*31 + d + 1000000000000) % 1000000007
		}
	}
	fmt.Printf("20 solves: checksum %d\n", check)
}
