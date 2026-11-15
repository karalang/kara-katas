// benchmark's Go mirror of halve.kara (LeetCode #2208, the ★ arm):
// greedily halve the largest number, kept in a container/heap max-heap of
// float64, until the halves taken add up to half the sum.
package main

import (
	"container/heap"
	"fmt"
)

type maxHeap []float64

func (h maxHeap) Len() int            { return len(h) }
func (h maxHeap) Less(i, j int) bool  { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x interface{}) { *h = append(*h, x.(float64)) }
func (h *maxHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func halveArray(nums []int64) int64 {
	h := &maxHeap{}
	total := 0.0
	for _, x := range nums {
		total += float64(x)
		heap.Push(h, float64(x))
	}
	removed := 0.0
	var ops int64
	for removed < total/2.0 {
		top := heap.Pop(h).(float64)
		half := top / 2.0
		removed += half
		heap.Push(h, half)
		ops++
	}
	return ops
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wideRandom(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	seed := int64(2208)
	tops := []int64{10, 1000, 10000000}
	arrays := [][]int64{}
	for a := 0; a < 12; a++ {
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = wideRandom(&seed)%tops[a%3] + 1
		}
		arrays = append(arrays, nums)
	}
	// each array halved once
	check := int64(0)
	for _, nums := range arrays {
		check = (check*31 + halveArray(nums)) % 1000000007
	}
	fmt.Printf("12 arrays of 10^5: checksum %d\n", check)
}
