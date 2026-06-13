// LeetCode #153 — Go goroutine-parallel mirror (par lane, binary_search).
// Same O(log n) find_min; the K=2_000_000-call reduction split across NumCPU
// workers (per-worker partial + merge). Hand-tuned-parallel comparator for
// Kāra's auto-par. Sink = 2000000 (K × min value 1).
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n = 2000000
	r = 666666
	k = 2000000
)

// Mirrors the seq lane's blackBox — keeps the compiler from hoisting the
// loop-invariant pure findMin out of the per-worker K-loop.
func blackBox[T any](v T) T { return v }

func findMin(nums []int64) int64 {
	lo := 0
	hi := len(nums) - 1
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] > nums[hi] {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return nums[lo]
}

func main() {
	data := make([]int64, n)
	for i := 0; i < n; i++ {
		data[i] = int64(((i+r)%n)+1)
	}

	workers := runtime.NumCPU()
	if workers > k {
		workers = k
	}
	chunk := k / workers
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)
	for w := 0; w < workers; w++ {
		go func(w int) {
			defer wg.Done()
			start := w * chunk
			end := start + chunk
			if w == workers-1 {
				end = k
			}
			var s int64
			for it := start; it < end; it++ {
				s += findMin(blackBox(data))
			}
			partials[w] = s
		}(w)
	}
	wg.Wait()
	var total int64
	for _, p := range partials {
		total += p
	}
	fmt.Println(total)
}
