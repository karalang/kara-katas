// Benchmark for #857: Minimum Cost to Hire K Workers -- the ★ arm,
// mirroring mincost_to_hire_workers.kara.
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

func mincostToHireWorkers(quality, wage []int64, k int64) float64 {
	n := len(quality)
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(x, y int) bool {
		a, b := order[x], order[y]
		return wage[a]*quality[b] < wage[b]*quality[a]
	})
	h := &maxHeap{}
	var sum int64
	var bestNum, bestDen int64 = -1, 1
	for _, i := range order {
		heap.Push(h, quality[i])
		sum += quality[i]
		if int64(h.Len()) > k {
			sum -= heap.Pop(h).(int64)
		}
		if int64(h.Len()) == k {
			num, den := wage[i]*sum, quality[i]
			if bestNum < 0 || num*bestDen < bestNum*den {
				bestNum, bestDen = num, den
			}
		}
	}
	return float64(bestNum) / float64(bestDen)
}

var seed int64 = 857

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds, n := 16, 600, 10000
	qualities := make([][]int64, count)
	wages := make([][]int64, count)
	for g := 0; g < count; g++ {
		for i := 0; i < n; i++ {
			qualities[g] = append(qualities[g], 1+nextRandom()%10000)
			wages[g] = append(wages[g], 1+nextRandom()%10000)
		}
	}
	total := 0.0
	for round := 0; round < rounds; round++ {
		g := round % count
		total += mincostToHireWorkers(qualities[g], wages[g], int64(1+g*600))
	}
	fmt.Printf("%d rounds of 16 sets: costs sum to %.5f\n", rounds, total)
}
