// Benchmark for #373 -- mirror of k_smallest_pairs.kara.
package main

import (
	"container/heap"
	"fmt"
)

type front struct{ sum, i, j int64 }

type fronts []front

func (h fronts) Len() int { return len(h) }
func (h fronts) Less(a, b int) bool {
	if h[a].sum != h[b].sum {
		return h[a].sum < h[b].sum
	}
	if h[a].i != h[b].i {
		return h[a].i < h[b].i
	}
	return h[a].j < h[b].j
}
func (h fronts) Swap(a, b int)       { h[a], h[b] = h[b], h[a] }
func (h *fronts) Push(x interface{}) { *h = append(*h, x.(front)) }
func (h *fronts) Pop() interface{} {
	old := *h
	f := old[len(old)-1]
	*h = old[:len(old)-1]
	return f
}

func kSmallestPairs(nums1, nums2 []int64, k int) [][2]int64 {
	out := [][2]int64{}
	if len(nums1) == 0 || len(nums2) == 0 {
		return out
	}
	h := &fronts{}
	for i := 0; i < len(nums1) && i < k; i++ {
		heap.Push(h, front{nums1[i] + nums2[0], int64(i), 0})
	}
	for len(out) < k && h.Len() > 0 {
		f := heap.Pop(h).(front)
		out = append(out, [2]int64{nums1[f.i], nums2[f.j]})
		if int(f.j)+1 < len(nums2) {
			heap.Push(h, front{nums1[f.i] + nums2[f.j+1], f.i, f.j + 1})
		}
	}
	return out
}

func main() {
	var seed, checksum int64 = 373, 0
	nums1 := make([]int64, 100000)
	nums2 := make([]int64, 100000)
	for round := 0; round < 20; round++ {
		var v int64 = -1000000000
		for i := range nums1 {
			seed = (seed*1103515245 + 12345) % 2147483648
			v += (seed / 65536) % 20000
			nums1[i] = v
		}
		v = -1000000000
		for i := range nums2 {
			seed = (seed*1103515245 + 12345) % 2147483648
			v += (seed / 65536) % 20000
			nums2[i] = v
		}
		for _, p := range kSmallestPairs(nums1, nums2, 10000) {
			checksum = (checksum*31 + (p[0]+p[1])%1000000007 + 2000000000) % 1000000007
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
