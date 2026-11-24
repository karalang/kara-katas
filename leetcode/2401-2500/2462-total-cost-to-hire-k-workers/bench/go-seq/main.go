// LeetCode #2462: Total Cost to Hire K Workers -- the bench, the ★ arm in
// Go: two `container/heap` min-heaps of `(cost, index)`, the first and
// the last `candidates` workers, each session taking the cheaper top and
// refilling its heap from the untaken middle.
package main

import (
	"container/heap"
	"fmt"
)

type item struct{ cost, index int64 }

type minHeap []item

func (h minHeap) Len() int { return len(h) }
func (h minHeap) Less(i, j int) bool {
	return h[i].cost < h[j].cost || (h[i].cost == h[j].cost && h[i].index < h[j].index)
}
func (h minHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x any)   { *h = append(*h, x.(item)) }
func (h *minHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func less(a, b item) bool {
	return a.cost < b.cost || (a.cost == b.cost && a.index < b.index)
}

func totalCost(costs []int64, k, candidates int64) int64 {
	n := int64(len(costs))
	front, back := &minHeap{}, &minHeap{}
	next, last := int64(0), n-1
	for next < candidates && next <= last {
		heap.Push(front, item{costs[next], next})
		next++
	}
	for n-1-last < candidates && next <= last {
		heap.Push(back, item{costs[last], last})
		last--
	}
	total := int64(0)
	for s := int64(0); s < k; s++ {
		takeFront := front.Len() > 0 && (back.Len() == 0 || !less((*back)[0], (*front)[0]))
		if takeFront {
			total += heap.Pop(front).(item).cost
			if next <= last {
				heap.Push(front, item{costs[next], next})
				next++
			}
		} else {
			total += heap.Pop(back).(item).cost
			if next <= last {
				heap.Push(back, item{costs[last], last})
				last--
			}
		}
	}
	return total
}

var seed int64 = 2462

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	// 10 lists of 10^5 costs from 1 to 10^5 built once; then 32 passes,
	// each setting one cost of every list from the checksum so far, then
	// answering every list with k of 5 10^4 and 1 + 97 p candidates,
	// folding the answer plus the pass into the checksum
	lists := make([][]int64, 10)
	for a := range lists {
		lists[a] = make([]int64, 100000)
		for i := range lists[a] {
			lists[a][i] = 1 + wideRandom()%100000
		}
	}
	check := int64(0)
	for p := int64(0); p < 32; p++ {
		candidates := 1 + 97*p
		for a := range lists {
			lists[a][(check+int64(a))%100000] = 1 + check%100000
			check = (check*31 + totalCost(lists[a], 50000, candidates) + p) % 1000000007
		}
	}
	fmt.Printf("32 passes over 10 lists of 10^5: checksum %d\n", check)
}
