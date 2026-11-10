// LeetCode #2093: Minimum Cost to Reach City With Discounts -- Go mirror of
// the ★ arm's benchmark (discounts.kara): the same 60 maps, each asked by
// the same Dijkstra over (city, used) states with a `container/heap`.
package main

import (
	"container/heap"
	"fmt"
	"math"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type item struct{ cost, city, used int64 }
type minHeap []item

func (h minHeap) Len() int { return len(h) }
func (h minHeap) Less(i, j int) bool {
	if h[i].cost != h[j].cost {
		return h[i].cost < h[j].cost
	}
	if h[i].city != h[j].city {
		return h[i].city < h[j].city
	}
	return h[i].used < h[j].used
}
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(item)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type road struct{ other, toll int64 }

func minimumCost(n int64, highways [][3]int64, discounts int64) int64 {
	roads := make([][]road, n)
	for _, h := range highways {
		roads[h[0]] = append(roads[h[0]], road{h[1], h[2]})
		roads[h[1]] = append(roads[h[1]], road{h[0], h[2]})
	}
	k := discounts + 1
	best := make([]int64, n*k)
	for i := range best {
		best[i] = math.MaxInt64
	}
	h := &minHeap{}
	best[0] = 0
	heap.Push(h, item{0, 0, 0})
	for h.Len() > 0 {
		it := heap.Pop(h).(item)
		cost, city, used := it.cost, it.city, it.used
		if city == n-1 {
			return cost
		}
		if cost > best[city*k+used] {
			continue
		}
		for _, r := range roads[city] {
			full := cost + r.toll
			if full < best[r.other*k+used] {
				best[r.other*k+used] = full
				heap.Push(h, item{full, r.other, used})
			}
			if used < discounts {
				half := cost + r.toll/2
				if half < best[r.other*k+used+1] {
					best[r.other*k+used+1] = half
					heap.Push(h, item{half, r.other, used + 1})
				}
			}
		}
	}
	return -1
}

func main() {
	seed := int64(2093)
	n := int64(20000)
	total := int64(0)
	check := int64(0)
	for g := int64(0); g < 60; g++ {
		highways := make([][3]int64, 0, 3*n)
		for a := int64(0); a < n; a++ {
			for _, base := range []int64{1, 1667, 3333} {
				b := (a + base + nextRandom(&seed)%1666) % n
				hi := nextRandom(&seed)
				toll := (hi*32768 + nextRandom(&seed)) % 100001
				highways = append(highways, [3]int64{a, b, toll})
			}
		}
		c := minimumCost(n, highways, g%12*2)
		total += c
		check = (check*31 + c + 2) % 1000000007
	}
	fmt.Printf("60 answers: sum %d, checksum %d\n", total, check)
}
