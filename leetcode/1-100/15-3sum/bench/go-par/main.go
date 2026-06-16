// LeetCode #15 — Go goroutine-parallel mirror (par lane, three_sum).
// Same sort + two-pointer dedup; the K=1M reduction is split across NumCPU
// workers (per-worker partial + merge). Hand-tuned-parallel comparator.
// Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sort"
	"sync"
)

const (
	mCases  = 8
	nValues = 16
	kIters  = 1000000
)

func threeSum(nums []int64) [][]int64 {
	s := make([]int64, len(nums))
	copy(s, nums)
	sort.Slice(s, func(a, b int) bool { return s[a] < s[b] })
	n := int64(len(s))
	result := [][]int64{}
	var i int64 = 0
	for i < n-2 {
		if i > 0 && s[i] == s[i-1] {
			i++
			continue
		}
		if s[i] > 0 {
			break
		}
		lo, hi := i+1, n-1
		for lo < hi {
			sum := s[i] + s[lo] + s[hi]
			if sum < 0 {
				lo++
			} else if sum > 0 {
				hi--
			} else {
				result = append(result, []int64{s[i], s[lo], s[hi]})
				lo++
				hi--
				for lo < hi && s[lo] == s[lo-1] {
					lo++
				}
				for lo < hi && s[hi] == s[hi+1] {
					hi--
				}
			}
		}
		i++
	}
	return result
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

func main() {
	sets := make([][]int64, mCases)
	for m := int64(0); m < mCases; m++ {
		sets[m] = buildCase(m*1000003+12345, nValues)
	}

	workers := runtime.NumCPU()
	if workers > kIters {
		workers = kIters
	}
	chunk := int64(kIters / workers)
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)
	for w := 0; w < workers; w++ {
		go func(w int) {
			defer wg.Done()
			start := int64(w) * chunk
			end := start + chunk
			if w == workers-1 {
				end = kIters
			}
			var s int64
			for k := start; k < end; k++ {
				idx := k % mCases
				r := threeSum(sets[idx])
				s += int64(len(r))
			}
			partials[w] = s
		}(w)
	}
	wg.Wait()
	var sum int64
	for _, p := range partials {
		sum += p
	}
	fmt.Println(sum)
}
