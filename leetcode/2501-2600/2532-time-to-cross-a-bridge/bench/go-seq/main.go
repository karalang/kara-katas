// LeetCode #2532: Time to Cross a Bridge -- benchmark mirror of the ★ arm
// (bridge.kara): 200 cases built once, then the passes, each asking every
// case from an offset the checksum picks. The four queues are
// container/heap heaps of (key, worker) pairs, two largest first and two
// smallest first.
package main

import (
	"container/heap"
	"fmt"
	"math"
)

type pair struct{ key, i int64 }

type pairs struct {
	a        []pair
	maxFirst bool
}

func (h pairs) Len() int { return len(h.a) }
func (h pairs) Less(x, y int) bool {
	p, q := h.a[x], h.a[y]
	if h.maxFirst {
		return p.key > q.key || (p.key == q.key && p.i > q.i)
	}
	return p.key < q.key || (p.key == q.key && p.i < q.i)
}
func (h pairs) Swap(x, y int) { h.a[x], h.a[y] = h.a[y], h.a[x] }
func (h *pairs) Push(x any)   { h.a = append(h.a, x.(pair)) }
func (h *pairs) Pop() any {
	last := h.a[len(h.a)-1]
	h.a = h.a[:len(h.a)-1]
	return last
}

func findCrossingTime(n, k int64, time [][4]int64) int64 {
	left := &pairs{maxFirst: true}
	right := &pairs{maxFirst: true}
	picking := &pairs{}
	putting := &pairs{}
	for i := int64(0); i < k; i++ {
		heap.Push(left, pair{time[i][0] + time[i][2], i})
	}
	boxes, now := n, int64(0)
	for boxes > 0 || right.Len() > 0 || picking.Len() > 0 {
		for putting.Len() > 0 && putting.a[0].key <= now {
			i := heap.Pop(putting).(pair).i
			heap.Push(left, pair{time[i][0] + time[i][2], i})
		}
		for picking.Len() > 0 && picking.a[0].key <= now {
			i := heap.Pop(picking).(pair).i
			heap.Push(right, pair{time[i][0] + time[i][2], i})
		}
		if right.Len() > 0 {
			i := heap.Pop(right).(pair).i
			now += time[i][2]
			heap.Push(putting, pair{now + time[i][3], i})
		} else if boxes > 0 && left.Len() > 0 {
			i := heap.Pop(left).(pair).i
			now += time[i][0]
			boxes--
			heap.Push(picking, pair{now + time[i][1], i})
		} else {
			next := int64(math.MaxInt64)
			if picking.Len() > 0 && picking.a[0].key < next {
				next = picking.a[0].key
			}
			if boxes > 0 && putting.Len() > 0 && putting.a[0].key < next {
				next = putting.a[0].key
			}
			now = next
		}
	}
	return now
}

var seed int64 = 2532

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	ns := make([]int64, 200)
	ks := make([]int64, 200)
	times := make([][][4]int64, 200)
	for t := 0; t < 200; t++ {
		ns[t] = nextRandom()%1000 + 1
		ks[t] = nextRandom()%100 + 1
		times[t] = make([][4]int64, ks[t])
		for i := range times[t] {
			for j := 0; j < 4; j++ {
				times[t][i][j] = nextRandom()%1000 + 1
			}
		}
	}
	const passes = 100
	var check int64
	for p := int64(0); p < passes; p++ {
		start := check % 200
		for i := int64(0); i < 200; i++ {
			at := (start + i) % 200
			check = (check*31 + findCrossingTime(ns[at], ks[at], times[at]) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 200 cases: checksum %d\n", passes, check)
}
