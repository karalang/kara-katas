// LeetCode #7 — Go goroutine-parallel mirror (par lane, reverse).
// Same pop-and-push reverse; the K=50M reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n      = 1024
	kIters = 50_000_000
)

func reverse(x int32) int32 {
	var result int32
	const intMax int32 = 2147483647
	const intMin int32 = -2147483648
	const maxDiv int32 = intMax / 10
	const minDiv int32 = intMin / 10

	for x != 0 {
		digit := x % 10
		if result > maxDiv || (result == maxDiv && digit > 7) {
			return 0
		}
		if result < minDiv || (result == minDiv && digit < -8) {
			return 0
		}
		result = result*10 + digit
		x /= 10
	}
	return result
}

func main() {
	inputs := make([]int32, n)
	for i := int64(0); i < n; i++ {
		raw := i*2654435769 + 305419896
		inputs[i] = int32(raw)
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
				s += int64(reverse(inputs[idx]))
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
