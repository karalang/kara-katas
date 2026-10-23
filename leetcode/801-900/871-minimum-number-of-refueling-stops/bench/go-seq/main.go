// LeetCode #871: Minimum Number of Refueling Stops -- Go mirror of the
// bench program (the ★ arm, a heap of the stations passed), with
// container/heap as the Kāra program has a max-first PriorityQueue.
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
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type station struct{ pos, fuel int64 }

func minRefuelStops(target, startFuel int64, stations []station) int64 {
	passed := &maxHeap{}
	reach := startFuel
	var stops int64
	next := 0
	for reach < target {
		for next < len(stations) && stations[next].pos <= reach {
			heap.Push(passed, stations[next].fuel)
			next++
		}
		if passed.Len() == 0 {
			return -1
		}
		reach += heap.Pop(passed).(int64)
		stops++
	}
	return stops
}

var seed int64 = 871

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomBelow(limit int64) int64 {
	hi := nextRandom()
	lo := nextRandom()
	return (hi*32768 + lo) % limit
}

func main() {
	var total, unreachable, check int64
	for r := 0; r < 100; r++ {
		target := randomBelow(500000000) + 500000001
		positions := make([]int64, 0, 500)
		for i := 0; i < 500; i++ {
			positions = append(positions, randomBelow(target-1)+1)
		}
		sort.Slice(positions, func(a, b int) bool { return positions[a] < positions[b] })
		stations := []station{}
		for i, p := range positions {
			if i > 0 && positions[i-1] == p {
				continue
			}
			stations = append(stations, station{p, randomBelow(target/40) + 1})
		}
		for j := int64(0); j < 400; j++ {
			a := minRefuelStops(target, j*(target/800)+1, stations)
			if a < 0 {
				unreachable++
			} else {
				total += a
			}
			check = (check*31 + a + 1) % 1000000007
		}
	}
	fmt.Printf("40000 trips over 100 lists of 500 stations: stops sum to %d, %d unreachable, checksum %d\n", total, unreachable, check)
}
