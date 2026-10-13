// Benchmark for #502: Go mirror of the ★ arm (projects sorted by
// capital, profits in a heap); see ../ipo.kara. container/heap over a
// slice, ordered largest first.
package main

import (
	"cmp"
	"container/heap"
	"fmt"
	"slices"
)

type maxHeap []int64

func (h maxHeap) Len() int           { return len(h) }
func (h maxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x any)        { *h = append(*h, x.(int64)) }
func (h *maxHeap) Pop() any {
	old := *h
	v := old[len(old)-1]
	*h = old[:len(old)-1]
	return v
}

func findMaximizedCapital(k, w int64, profits, capital []int64) int64 {
	n := len(profits)
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	slices.SortStableFunc(order, func(a, b int) int { return cmp.Compare(capital[a], capital[b]) })
	ready := &maxHeap{}
	money := w
	next := 0
	for r := int64(0); r < k; r++ {
		for next < n && capital[order[next]] <= money {
			heap.Push(ready, profits[order[next]])
			next++
		}
		if ready.Len() == 0 {
			break
		}
		money += heap.Pop(ready).(int64)
	}
	return money
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 60 cases of 100,000 projects with k = 100,000, profits 0 to 10,000
	// and capital needs from 0 to 10^5, 10^7 or 10^9 in turn, w from 0
	// to 1,000; built once. Then each case is solved once.
	cases := 60
	n := 100000
	seed := int64(502)
	allProfits := make([][]int64, 0, cases)
	allCapital := make([][]int64, 0, cases)
	starts := make([]int64, 0, cases)
	for c := 0; c < cases; c++ {
		var scale int64
		if c%3 == 0 {
			scale = 100001
		} else if c%3 == 1 {
			scale = 10000001
		} else {
			scale = 1000000001
		}
		profits := make([]int64, n)
		capital := make([]int64, n)
		for i := 0; i < n; i++ {
			profits[i] = nextRandom(&seed) % 10001
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			capital[i] = (hi*32768 + lo) % scale
		}
		allProfits = append(allProfits, profits)
		allCapital = append(allCapital, capital)
		starts = append(starts, nextRandom(&seed)%1001)
	}
	total, checksum := int64(0), int64(0)
	for c := 0; c < cases; c++ {
		got := findMaximizedCapital(int64(n), starts[c], allProfits[c], allCapital[c])
		total += got
		checksum = (checksum*31 + got) % 1000000007
	}
	fmt.Printf("%d cases of %d projects: total capital %d, checksum %d\n", cases, n, total, checksum)
}
