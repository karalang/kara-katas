// LeetCode #630: Course Schedule III -- Go mirror of the Kāra bench.
//
// The ★ arm's greedy over the same inputs and rounds: the course
// slice copied and sorted by last day, and a max-heap of the durations
// taken through container/heap.
package main

import (
	"container/heap"
	"fmt"
	"sort"
)

type maxHeap []int64

func (h maxHeap) Len() int            { return len(h) }
func (h maxHeap) Less(i, j int) bool  { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x interface{}) { *h = append(*h, x.(int64)) }
func (h *maxHeap) Pop() interface{} {
	old := *h
	v := old[len(old)-1]
	*h = old[:len(old)-1]
	return v
}

func scheduleCourse(courses [][]int64) int64 {
	order := append([][]int64(nil), courses...)
	sort.Slice(order, func(a, b int) bool { return order[a][1] < order[b][1] })
	taken := &maxHeap{}
	var time int64
	for _, course := range order {
		time += course[0]
		heap.Push(taken, course[0])
		if time > course[1] {
			time -= heap.Pop(taken).(int64)
		}
	}
	return int64(taken.Len())
}

var seed int64 = 630

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const inputs = 20
	const rounds = 200
	all := make([][][]int64, 0, inputs)
	for i := 0; i < inputs; i++ {
		longest := 10 + nextRandom()%991
		courses := make([][]int64, 0, 10000)
		for j := 0; j < 10000; j++ {
			duration := 1 + nextRandom()%longest
			last := 1 + nextRandom()%10000
			courses = append(courses, []int64{duration, last})
		}
		all = append(all, courses)
	}
	var sum, checksum int64
	for r := 0; r < rounds; r++ {
		c := scheduleCourse(all[(r*7)%inputs])
		sum += c
		checksum = (checksum*31 + c) % 1000000007
	}
	fmt.Printf("%d inputs, %d rounds: total %d, checksum %d\n", inputs, rounds, sum, checksum)
}
