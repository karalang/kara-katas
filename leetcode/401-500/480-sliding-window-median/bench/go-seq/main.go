// Benchmark for #480: Go mirror of the ★ arm (two heaps, deletions put
// off); see ../sliding_window_median.kara.
package main

import (
	"container/heap"
	"fmt"
)

// A min-heap of int64; the low half stores negated values.
type minHeap []int64

func (h minHeap) Len() int            { return len(h) }
func (h minHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(int64)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type window struct {
	low, high         minHeap
	gone              map[int64]int64
	lowSize, highSize int64
}

func (w *window) prune() {
	for w.low.Len() > 0 {
		top := -w.low[0]
		left := w.gone[top]
		if left == 0 {
			break
		}
		w.gone[top] = left - 1
		heap.Pop(&w.low)
	}
	for w.high.Len() > 0 {
		top := w.high[0]
		left := w.gone[top]
		if left == 0 {
			break
		}
		w.gone[top] = left - 1
		heap.Pop(&w.high)
	}
}

func (w *window) balance() {
	if w.lowSize > w.highSize+1 {
		x := -heap.Pop(&w.low).(int64)
		heap.Push(&w.high, x)
		w.lowSize--
		w.highSize++
	} else if w.lowSize < w.highSize {
		x := heap.Pop(&w.high).(int64)
		heap.Push(&w.low, -x)
		w.highSize--
		w.lowSize++
	}
	w.prune()
}

func (w *window) add(x int64) {
	if w.low.Len() == 0 || x <= -w.low[0] {
		heap.Push(&w.low, -x)
		w.lowSize++
	} else {
		heap.Push(&w.high, x)
		w.highSize++
	}
	w.balance()
}

func (w *window) remove(x int64) {
	inLow := x <= -w.low[0]
	w.gone[x]++
	if inLow {
		w.lowSize--
	} else {
		w.highSize--
	}
	w.prune()
	w.balance()
}

func (w *window) median(k int) float64 {
	a := -w.low[0]
	if k%2 == 1 {
		return float64(a)
	}
	return float64(a+w.high[0]) / 2.0
}

func medianSlidingWindow(nums []int64, k int) []float64 {
	w := &window{gone: map[int64]int64{}}
	var medians []float64
	for i := range nums {
		w.add(nums[i])
		if i >= k {
			w.remove(nums[i-k])
		}
		if i >= k-1 {
			medians = append(medians, w.median(k))
		}
	}
	return medians
}

var seed int64 = 480

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := 1000000
	nums := make([]int64, 0, n)
	for i := 0; i < n; i++ {
		a := nextRandom()
		b := nextRandom()
		r := a*32768 + b
		nums = append(nums, r*4+nextRandom()%4-2147483648)
	}
	var windows, checksum int64
	for k := 1000; k < 1002; k++ {
		for _, m := range medianSlidingWindow(nums, k) {
			windows++
			checksum = (checksum*31 + int64(m*2.0)%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("%d windows: checksum %d\n", windows, checksum)
}
