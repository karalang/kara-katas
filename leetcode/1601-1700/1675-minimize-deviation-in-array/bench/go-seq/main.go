// LeetCode #1675: Minimize Deviation in Array -- the bench's Go mirror: the
// ★ arm on 50 arrays of 50000 values up to 10^9, all drawn first, each
// answered 10 times, with container/heap over a max-first slice.

package main

import (
	"container/heap"
	"fmt"
	"math"
)

type maxHeap []int32

func (h maxHeap) Len() int           { return len(h) }
func (h maxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x any)        { *h = append(*h, x.(int32)) }
func (h *maxHeap) Pop() any {
	old := *h
	v := old[len(old)-1]
	*h = old[:len(old)-1]
	return v
}

func minimumDeviation(nums []int32) int32 {
	queue := make(maxHeap, 0, len(nums))
	smallest := int32(math.MaxInt32)
	for _, x := range nums {
		start := x
		if x%2 == 1 {
			start = x * 2
		}
		heap.Push(&queue, start)
		smallest = min(smallest, start)
	}
	best := int32(math.MaxInt32)
	for {
		top := heap.Pop(&queue).(int32)
		best = min(best, top-smallest)
		if top%2 == 1 {
			break
		}
		smallest = min(smallest, top/2)
		heap.Push(&queue, top/2)
	}
	return best
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1675

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const arrays = 50
	const n = 50000
	const rounds = 10
	cases := make([][]int32, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32((nextRandom()*32768+nextRandom())%1000000000 + 1)
		}
		cases = append(cases, nums)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range cases {
			deviation := int64(minimumDeviation(nums))
			total += deviation
			check = (check*31 + deviation + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: deviations sum to %d, checksum %d\n", arrays, n, rounds, total, check)
}
