// LeetCode #1845: Seat Reservation Manager -- the bench in Go: the ★ arm,
// every unreserved seat in a container/heap min-heap, over 50 runs of 10^5
// calls on 50000 to 99999 seats, each run's size and its place in one list
// of 10^6 draws, built once, taken from the checksum so far. A draw reserves
// a seat two times in three, and otherwise gives back a held seat it picks;
// every seat reserved goes into the checksum.
package main

import (
	"container/heap"
	"fmt"
)

type seatHeap []int64

func (h seatHeap) Len() int            { return len(h) }
func (h seatHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h seatHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *seatHeap) Push(x interface{}) { *h = append(*h, x.(int64)) }
func (h *seatHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type SeatManager struct {
	free *seatHeap
}

func Constructor(n int64) SeatManager {
	h := make(seatHeap, n)
	for i := int64(0); i < n; i++ {
		h[i] = i + 1
	}
	heap.Init(&h)
	return SeatManager{&h}
}

func (m *SeatManager) Reserve() int64 {
	return heap.Pop(m.free).(int64)
}

func (m *SeatManager) Unreserve(seatNumber int64) {
	heap.Push(m.free, seatNumber)
}

func main() {
	seed := int64(1845)
	draws := make([]int64, 1000000)
	for i := range draws {
		seed = (seed*1103515245 + 12345) % 2147483648
		draws[i] = seed / 65536
	}
	check := int64(0)
	for run := 0; run < 50; run++ {
		n := 50000 + check%50000
		start := check % 500000
		seats := Constructor(n)
		held := make([]int64, 0, 100000)
		for k := int64(0); k < 100000; k++ {
			d := draws[start+k]
			if len(held) == 0 || (d%3 != 0 && int64(len(held)) < n) {
				seat := seats.Reserve()
				check = (check*31 + seat) % 1000000007
				held = append(held, seat)
			} else {
				i := d % int64(len(held))
				seat := held[i]
				held[i] = held[len(held)-1]
				held = held[:len(held)-1]
				seats.Unreserve(seat)
			}
		}
	}
	fmt.Printf("50 runs: checksum %d\n", check)
}
