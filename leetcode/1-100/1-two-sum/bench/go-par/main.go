// LeetCode #1 — Go goroutine-parallel mirror (par lane, brute_force).
// Same O(n²) two_sum; the 100-call reduction is split across NumCPU workers
// (per-worker partial + merge). Hand-tuned-parallel comparator. Sink = -200.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n     = 5000
	iters = 100
)

func twoSum(nums []int64, target int64) (int, int, bool) {
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if nums[i]+nums[j] == target {
				return i, j, true
			}
		}
	}
	return 0, 0, false
}

func main() {
	data := make([]int64, n)
	for i := 0; i < n; i++ {
		data[i] = (int64(i) * 7) % 1000
	}
	var target int64 = -1

	workers := runtime.NumCPU()
	if workers > iters {
		workers = iters
	}
	chunk := iters / workers
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)
	for w := 0; w < workers; w++ {
		go func(w int) {
			defer wg.Done()
			start := w * chunk
			end := start + chunk
			if w == workers-1 {
				end = iters
			}
			var s int64
			for k := start; k < end; k++ {
				if i, j, ok := twoSum(data, target); ok {
					s += int64(i) + int64(j)
				} else {
					s += -2
				}
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
