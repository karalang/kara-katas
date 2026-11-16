// LeetCode #1172: Dinner Plate Stacks -- the ★ arm's bench in Go: the
// stacks in a slice of slices and a container/heap min-heap of the indices
// that may have room, an index whose stack is full or gone dropped when it
// comes to the top. The same 60 streams of 200000 calls.
package main

import (
	"container/heap"
	"fmt"
)

type IntHeap []int

func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *IntHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *IntHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type DinnerPlates struct {
	capacity int
	stacks   [][]int64
	open     IntHeap
}

func (d *DinnerPlates) Push(val int64) {
	for d.open.Len() > 0 {
		i := d.open[0]
		if i < len(d.stacks) && len(d.stacks[i]) < d.capacity {
			break
		}
		heap.Pop(&d.open)
	}
	if d.open.Len() == 0 {
		heap.Push(&d.open, len(d.stacks))
		d.stacks = append(d.stacks, nil)
	}
	i := d.open[0]
	d.stacks[i] = append(d.stacks[i], val)
	if len(d.stacks[i]) == d.capacity {
		heap.Pop(&d.open)
	}
}

func (d *DinnerPlates) Pop() int64 {
	if len(d.stacks) == 0 {
		return -1
	}
	return d.PopAtStack(len(d.stacks) - 1)
}

func (d *DinnerPlates) PopAtStack(index int) int64 {
	if index >= len(d.stacks) || len(d.stacks[index]) == 0 {
		return -1
	}
	s := d.stacks[index]
	val := s[len(s)-1]
	d.stacks[index] = s[:len(s)-1]
	heap.Push(&d.open, index)
	for len(d.stacks) > 0 && len(d.stacks[len(d.stacks)-1]) == 0 {
		d.stacks[len(d.stacks)-1] = nil
		d.stacks = d.stacks[:len(d.stacks)-1]
	}
	return val
}

var seed int64 = 1172

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	streams, calls := 60, 200000
	capacities := []int{1, 7, 100, 20000}
	var pops, misses, check int64
	for s := 0; s < streams; s++ {
		capacity := capacities[s%4]
		spread := int64(20000/capacity + 1)
		d := &DinnerPlates{capacity: capacity}
		for c := 0; c < calls; c++ {
			r := nextRandom() % 10
			var got int64
			if r < 6 {
				d.Push(1 + nextRandom()%20000)
				continue
			} else if r < 8 {
				got = d.Pop()
			} else {
				got = d.PopAtStack(int(nextRandom() % spread))
			}
			pops++
			if got == -1 {
				misses++
			}
			check = (check*131 + got + 2) % 1000000007
		}
	}
	fmt.Printf("%d streams of %d calls: %d pops, %d empty, checksum %d\n", streams, calls, pops, misses, check)
}
