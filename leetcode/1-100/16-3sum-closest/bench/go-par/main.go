// LeetCode #16 — Go goroutine-parallel mirror (par lane, 3Sum Closest).
// Same sort + two-pointer threeSumClosest; the K=1M reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sort"
	"sync"
)

func absI64(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func threeSumClosest(nums []int64, target int64) int64 {
	s := make([]int64, len(nums))
	copy(s, nums)
	sort.Slice(s, func(a, b int) bool { return s[a] < s[b] })
	n := int64(len(s))
	best := s[0] + s[1] + s[2]
	var i int64 = 0
	for i < n-2 {
		lo, hi := i+1, n-1
		for lo < hi {
			sum := s[i] + s[lo] + s[hi]
			if sum == target {
				return sum
			}
			if absI64(sum-target) < absI64(best-target) {
				best = sum
			}
			if sum < target {
				lo++
			} else {
				hi--
			}
		}
		i++
	}
	return best
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
func lcgNext(state int64) int64 {
	return (1103515245*state + 12345) % 2147483648
}

func buildCase(seed, count int64) []int64 {
	v := make([]int64, 0, count)
	state := seed
	for j := int64(0); j < count; j++ {
		state = lcgNext(state)
		v = append(v, (state%21)-10)
	}
	return v
}

var targetBag = [8]int64{-12, -6, -1, 0, 1, 5, 11, 19}

func targetFor(idx int64) int64 {
	return targetBag[idx]
}

func main() {
	const mCases int64 = 8
	const nValues int64 = 16
	const kIters int64 = 1000000

	sets := make([][]int64, mCases)
	for m := int64(0); m < mCases; m++ {
		sets[m] = buildCase(m*1000003+12345, nValues)
	}

	workers := runtime.NumCPU()
	if int64(workers) > kIters {
		workers = int(kIters)
	}
	chunk := kIters / int64(workers)
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
				idx := k % mCases
				s += threeSumClosest(sets[idx], targetFor(idx))
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
