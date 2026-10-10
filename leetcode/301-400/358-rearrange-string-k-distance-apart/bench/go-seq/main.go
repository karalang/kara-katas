// Benchmark for #358 -- mirror of rearrange.kara.
package main

import (
	"container/heap"
	"fmt"
)

type item struct{ left, neg int64 }

// maxHeap pops the largest (left, neg) first.
type maxHeap []item

func (h maxHeap) Len() int { return len(h) }
func (h maxHeap) Less(i, j int) bool {
	return h[i].left > h[j].left || (h[i].left == h[j].left && h[i].neg > h[j].neg)
}
func (h maxHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x interface{}) { *h = append(*h, x.(item)) }
func (h *maxHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

func rearrange(s []byte, k int64) []byte {
	var counts [26]int64
	for _, b := range s {
		counts[b-'a']++
	}
	ready := &maxHeap{}
	for c := 0; c < 26; c++ {
		if counts[c] > 0 {
			heap.Push(ready, item{counts[c], -int64(c)})
		}
	}
	var cooling []item
	out := make([]byte, 0, len(s))
	for range s {
		if ready.Len() == 0 {
			return nil
		}
		it := heap.Pop(ready).(item)
		c := -it.neg
		out = append(out, byte(c)+'a')
		cooling = append(cooling, item{it.left - 1, c})
		if int64(len(cooling)) >= k {
			f := cooling[0]
			cooling = cooling[1:]
			if f.left > 0 {
				heap.Push(ready, item{f.left, -f.neg})
			}
		}
	}
	return out
}

func main() {
	var seed int64 = 358
	possible := 0
	var checksum int64
	for round := 0; round < 200; round++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		width := (seed/65536)%23 + 4
		seed = (seed*1103515245 + 12345) % 2147483648
		k := (seed/65536)%8 + 1
		s := make([]byte, 0, 50000)
		for i := 0; i < 50000; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			draw := seed / 65536
			var c int64
			if draw%8 != 0 {
				c = (draw / 8) % width
			}
			s = append(s, byte(c)+'a')
		}
		r := rearrange(s, k)
		if len(r) == len(s) {
			possible++
		}
		for _, b := range r {
			checksum = (checksum*31 + int64(b)) % 1000000007
		}
		checksum = (checksum*31 + 7) % 1000000007
	}
	fmt.Printf("%d of 200 strings can be arranged, checksum %d\n", possible, checksum)
}
