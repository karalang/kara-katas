// LeetCode 295 benchmark lane — Go mirror of medianfinder.kara.
//
// Hand-rolled heap rather than container/heap, matching the C and Rust mirrors:
// container/heap dispatches through an interface per comparison, which would
// measure Go's devirtualisation rather than the algorithm. Same `max` flag
// instead of negation, same workload, same sink.
package main

import "fmt"

type Heap struct {
	data []int64
	max  bool
}

func newHeap(max bool) *Heap {
	return &Heap{data: make([]int64, 0, 1024), max: max}
}

func (h *Heap) outranks(a, b int64) bool {
	if h.max {
		return a > b
	}
	return a < b
}

func (h *Heap) push(v int64) {
	h.data = append(h.data, v)
	i := len(h.data) - 1
	for i > 0 {
		parent := (i - 1) / 2
		if !h.outranks(h.data[i], h.data[parent]) {
			break
		}
		h.data[i], h.data[parent] = h.data[parent], h.data[i]
		i = parent
	}
}

func (h *Heap) pop() int64 {
	top := h.data[0]
	last := h.data[len(h.data)-1]
	h.data = h.data[:len(h.data)-1]
	if len(h.data) > 0 {
		h.data[0] = last
		n := len(h.data)
		i := 0
		for {
			l := 2*i + 1
			r := l + 1
			best := i
			if l < n && h.outranks(h.data[l], h.data[best]) {
				best = l
			}
			if r < n && h.outranks(h.data[r], h.data[best]) {
				best = r
			}
			if best == i {
				break
			}
			h.data[i], h.data[best] = h.data[best], h.data[i]
			i = best
		}
	}
	return top
}

func main() {
	const n int64 = 2000000
	lo := newHeap(true)
	hi := newHeap(false)

	var state int64 = 12345
	var checksum int64 = 0
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 0x7fffffff
		v := state%1000003 - 500000

		lo.push(v)
		hi.push(lo.pop())
		if len(hi.data) > len(lo.data) {
			lo.push(hi.pop())
		}

		var twice int64
		if len(lo.data) > len(hi.data) {
			twice = 2 * lo.data[0]
		} else {
			twice = lo.data[0] + hi.data[0]
		}
		checksum = (checksum*31 + twice) % 1000000007
	}

	fmt.Printf("adds %d checksum %d\n", n, checksum)
}
