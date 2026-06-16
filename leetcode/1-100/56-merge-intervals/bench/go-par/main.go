// LeetCode #56 — Go goroutine-parallel mirror (par lane, merge_intervals).
// Same merge_intervals (sort-by-first-component + sweep); the K=1M
// reduction is split across NumCPU workers (per-worker partial + merge).
// Hand-tuned-parallel comparator. Sink matches the kara/rust/c/go mirrors.
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
	kIters  = 1_000_000
)

type interval struct {
	start int64
	end   int64
}

func mergeIntervals(intervals []interval) int64 {
	s := make([]interval, len(intervals))
	copy(s, intervals)
	sort.SliceStable(s, func(a, b int) bool { return s[a].start < s[b].start })
	if len(s) == 0 {
		return 0
	}
	var count int64 = 0
	curStart := s[0].start
	curEnd := s[0].end
	for i := 1; i < len(s); i++ {
		if s[i].start <= curEnd {
			if s[i].end > curEnd {
				curEnd = s[i].end
			}
		} else {
			count++
			curStart = s[i].start
			curEnd = s[i].end
		}
	}
	_ = curStart
	count++
	return count
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
func lcgNext(state int64) int64 {
	return (1103515245*state + 12345) % 2147483648
}

func buildCase(seed int64, count int64) []interval {
	v := make([]interval, 0, count)
	state := seed
	for j := int64(0); j < count; j++ {
		state = lcgNext(state)
		start := state % 51
		state = lcgNext(state)
		width := (state % 10) + 1
		v = append(v, interval{start: start, end: start + width})
	}
	return v
}

func main() {
	sets := make([][]interval, mCases)
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
				s += mergeIntervals(sets[idx])
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
