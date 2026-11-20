// LeetCode #2406: Divide Intervals Into Minimum Number of Groups -- the
// bench, the ★ arm in Go: the intervals copied and sorted by left end with
// `sort.Slice`, and a binary min-heap of each group's last right end.

package main

import (
	"fmt"
	"sort"
)

var seed int64 = 2406

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type interval struct{ left, right int64 }

func minGroups(iv []interval) int64 {
	order := append([]interval(nil), iv...)
	sort.Slice(order, func(a, b int) bool {
		if order[a].left != order[b].left {
			return order[a].left < order[b].left
		}
		return order[a].right < order[b].right
	})
	heap := make([]int64, 0, len(order))
	for _, x := range order {
		if len(heap) > 0 && heap[0] < x.left {
			n := len(heap) - 1
			heap[0] = heap[n]
			heap = heap[:n]
			i := 0
			for {
				l, r, m := 2*i+1, 2*i+2, i
				if l < n && heap[l] < heap[m] {
					m = l
				}
				if r < n && heap[r] < heap[m] {
					m = r
				}
				if m == i {
					break
				}
				heap[i], heap[m] = heap[m], heap[i]
				i = m
			}
		}
		heap = append(heap, x.right)
		for i := len(heap) - 1; i > 0 && heap[(i-1)/2] > heap[i]; i = (i - 1) / 2 {
			heap[i], heap[(i-1)/2] = heap[(i-1)/2], heap[i]
		}
	}
	return int64(len(heap))
}

func main() {
	sets := make([][]interval, 10)
	for i := range sets {
		iv := make([]interval, 100000)
		for j := range iv {
			left := 1 + (nextRandom()*32768+nextRandom())%900000
			iv[j] = interval{left, left + (nextRandom()*32768+nextRandom())%(1+1000*int64(i))}
		}
		sets[i] = iv
	}
	var check int64
	for p := int64(0); p < 5; p++ {
		for _, iv := range sets {
			check = (check*31 + minGroups(iv) + p) % 1000000007
		}
	}
	fmt.Printf("5 passes over 10 sets of 10^5 intervals: checksum %d\n", check)
}
