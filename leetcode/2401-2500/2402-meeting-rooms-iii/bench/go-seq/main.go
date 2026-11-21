// LeetCode #2402: Meeting Rooms III -- the bench, the ★ arm in Go: a
// container/heap of free rooms and one of (end, room) for the rooms in
// use, over the meetings sorted by start.

package main

import (
	"container/heap"
	"fmt"
	"sort"
)

type pair struct{ a, b int64 }

func less(x, y pair) bool { return x.a < y.a || (x.a == y.a && x.b < y.b) }

type pairHeap []pair

func (h pairHeap) Len() int            { return len(h) }
func (h pairHeap) Less(i, j int) bool  { return less(h[i], h[j]) }
func (h pairHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *pairHeap) Push(x interface{}) { *h = append(*h, x.(pair)) }
func (h *pairHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

var seed int64 = 2402

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mostBooked(n int64, meetings []pair) int64 {
	order := append([]pair(nil), meetings...)
	sort.Slice(order, func(i, j int) bool { return less(order[i], order[j]) })
	free := &pairHeap{}
	for r := int64(0); r < n; r++ {
		heap.Push(free, pair{r, 0})
	}
	busy := &pairHeap{}
	count := make([]int64, n)
	for _, m := range order {
		start, end := m.a, m.b
		for busy.Len() > 0 && (*busy)[0].a <= start {
			p := heap.Pop(busy).(pair)
			heap.Push(free, pair{p.b, 0})
		}
		if free.Len() > 0 {
			room := heap.Pop(free).(pair).a
			count[room]++
			heap.Push(busy, pair{end, room})
		} else {
			p := heap.Pop(busy).(pair)
			count[p.b]++
			heap.Push(busy, pair{p.a + end - start, p.b})
		}
	}
	best := int64(0)
	for r := int64(1); r < n; r++ {
		if count[r] > count[best] {
			best = r
		}
	}
	return best
}

func main() {
	cases := make([][]pair, 10)
	starts := make([]int64, 500000)
	for c := int64(0); c < 10; c++ {
		for i := range starts {
			starts[i] = int64(i)
		}
		for i := int64(0); i < 100000; i++ {
			hi := nextRandom()
			j := i + (hi*32768+nextRandom())%(500000-i)
			starts[i], starts[j] = starts[j], starts[i]
		}
		ms := make([]pair, 100000)
		for i := range ms {
			ms[i] = pair{starts[i], starts[i] + 1 + nextRandom()%(1+500*c)}
		}
		cases[c] = ms
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for _, ms := range cases {
			check = (check*31 + mostBooked(100, ms) + p) % 1000000007
		}
	}
	fmt.Printf("10 passes over 10 cases of 10^5 meetings in 100 rooms: checksum %d\n", check)
}
