// LeetCode #11 — Go goroutine-parallel mirror (par lane, container).
// Same two-pointer max_area_off; the K=10M reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n      = 8
	w      = 16
	total  = n * w
	kIters = 10_000_000
)

func maxAreaOff(heights []int64, lo int64, hi int64) int64 {
	l := lo
	r := hi
	var best int64 = 0
	for l < r {
		hL := heights[l]
		hR := heights[r]
		var h int64
		if hL < hR {
			h = hL
		} else {
			h = hR
		}
		area := h * (r - l)
		if area > best {
			best = area
		}
		if hL < hR {
			l += 1
		} else {
			r -= 1
		}
	}
	return best
}

func main() {
	heights := make([]int64, total)
	for i := int64(0); i < total; i++ {
		raw := i*2654435769 + 305419896
		v := ((raw % 50) + 50) % 50
		heights[i] = v
	}

	workers := runtime.NumCPU()
	if workers > kIters {
		workers = kIters
	}
	chunk := int64(kIters / workers)
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)
	for wk := 0; wk < workers; wk++ {
		go func(wk int) {
			defer wg.Done()
			start := int64(wk) * chunk
			end := start + chunk
			if wk == workers-1 {
				end = kIters
			}
			var s int64
			for k := start; k < end; k++ {
				idx := k % n
				lo := idx * w
				hi := lo + w - 1
				s += maxAreaOff(heights, lo, hi)
			}
			partials[wk] = s
		}(wk)
	}
	wg.Wait()
	var sum int64
	for _, p := range partials {
		sum += p
	}
	fmt.Println(sum)
}
