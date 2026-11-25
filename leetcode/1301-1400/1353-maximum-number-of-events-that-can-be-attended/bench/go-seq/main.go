// LeetCode #1353 bench -- Go: a sweep over the days with a min-heap of the
// open events' last days.
package main

import (
	"container/heap"
	"fmt"
	"sort"
)

type minHeap []int32

func (h minHeap) Len() int            { return len(h) }
func (h minHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(int32)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	v := old[len(old)-1]
	*h = old[:len(old)-1]
	return v
}

func maxEvents(events [][2]int32) int {
	byStart := make([][2]int32, len(events))
	copy(byStart, events)
	sort.SliceStable(byStart, func(i, j int) bool { return byStart[i][0] < byStart[j][0] })
	ends := &minHeap{}
	next, attended := 0, 0
	day := int32(1)
	for next < len(byStart) || ends.Len() > 0 {
		if ends.Len() == 0 && byStart[next][0] > day {
			day = byStart[next][0]
		}
		for next < len(byStart) && byStart[next][0] == day {
			heap.Push(ends, byStart[next][1])
			next++
		}
		for ends.Len() > 0 && (*ends)[0] < day {
			heap.Pop(ends)
		}
		if ends.Len() > 0 {
			heap.Pop(ends)
			attended++
		}
		day++
	}
	return attended
}

func main() {
	var seed int64 = 1353
	next := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	sets := make([][][2]int32, 20)
	for k := range sets {
		sets[k] = make([][2]int32, 10000)
		for i := range sets[k] {
			start := 1 + next()%10000
			sets[k][i] = [2]int32{int32(start), int32(start + next()%30)}
		}
	}
	var check int64
	for r := int64(0); r < 600; r++ {
		k, at := check%20, (check/20)%10000
		start := 1 + (check/7)%10000
		sets[k][at] = [2]int32{int32(start), int32(start + (check/11)%30)}
		check = (check*31 + int64(maxEvents(sets[k])) + r) % 1000000007
	}
	fmt.Printf("600 rounds over 20 sets of 10^4 events: checksum %d\n", check)
}
