// LeetCode #1834: Single-Threaded CPU -- the bench in Go: the ★ arm over
// 50 calls on the first 50000 to 99999 of one list of 10^5 tasks, built once,
// each coming in at 1 to 10^6 and taking 1 to 10^4, each run's length drawn
// from the checksum so far. Each call copies its run, a list of two-number
// lists, as the arm takes its list by value, and the order is folded into
// the checksum.
package main

import (
	"container/heap"
	"fmt"
	"sort"
)

type ready [][2]int64

func (h ready) Len() int { return len(h) }
func (h ready) Less(a, b int) bool {
	return h[a][0] < h[b][0] || (h[a][0] == h[b][0] && h[a][1] < h[b][1])
}
func (h ready) Swap(a, b int) { h[a], h[b] = h[b], h[a] }
func (h *ready) Push(x any)   { *h = append(*h, x.([2]int64)) }
func (h *ready) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func getOrder(tasks [][]int64) []int64 {
	n := len(tasks)
	coming := make([]int64, n)
	for i := range coming {
		coming[i] = int64(i)
	}
	sort.SliceStable(coming, func(a, b int) bool { return tasks[coming[a]][0] < tasks[coming[b]][0] })
	q := &ready{}
	order := make([]int64, 0)
	var clock int64
	next := 0
	for len(order) < n {
		if q.Len() == 0 && clock < tasks[coming[next]][0] {
			clock = tasks[coming[next]][0]
		}
		for next < n && tasks[coming[next]][0] <= clock {
			i := coming[next]
			heap.Push(q, [2]int64{tasks[i][1], i})
			next++
		}
		r := heap.Pop(q).([2]int64)
		clock += r[0]
		order = append(order, r[1])
	}
	return order
}

func main() {
	seed := int64(1834)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	base := make([][]int64, 0, 100000)
	for k := 0; k < 100000; k++ {
		hi := nextRandom()
		enqueue := 1 + (hi*32768+nextRandom())%1000000
		processing := 1 + nextRandom()%10000
		base = append(base, []int64{enqueue, processing})
	}
	var check int64
	for call := int64(0); call < 50; call++ {
		n := 50000 + (check+call)%50000
		run := make([][]int64, n)
		for k := range run {
			run[k] = []int64{base[k][0], base[k][1]}
		}
		for _, i := range getOrder(run) {
			check = (check*31 + i + 1) % 1000000007
		}
	}
	fmt.Printf("50 calls: checksum %d\n", check)
}
