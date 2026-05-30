// Benchmark workload — Merge Intervals (LeetCode #56).
// Go mirror of ../merge_intervals.kara. Same M/N/K, LCG generator,
// per-case (start, end) shape, sort-by-first-component + sweep, and sink
// — see that file's header for the rationale.

package main

import (
	"fmt"
	"sort"
)

type Interval struct {
	Start int64
	End   int64
}

func mergeIntervals(intervals []Interval) []Interval {
	s := make([]Interval, len(intervals))
	copy(s, intervals)
	sort.Slice(s, func(a, b int) bool { return s[a].Start < s[b].Start })
	result := []Interval{}
	n := len(s)
	if n == 0 {
		return result
	}
	curStart, curEnd := s[0].Start, s[0].End
	for i := 1; i < n; i++ {
		if s[i].Start <= curEnd {
			if s[i].End > curEnd {
				curEnd = s[i].End
			}
		} else {
			result = append(result, Interval{curStart, curEnd})
			curStart, curEnd = s[i].Start, s[i].End
		}
	}
	result = append(result, Interval{curStart, curEnd})
	return result
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
func lcgNext(state int64) int64 {
	return (1103515245*state + 12345) % 2147483648
}

func buildCase(seed, count int64) []Interval {
	v := make([]Interval, 0, count)
	state := seed
	for j := int64(0); j < count; j++ {
		state = lcgNext(state)
		start := state % 51
		state = lcgNext(state)
		width := (state % 10) + 1
		v = append(v, Interval{start, start + width})
	}
	return v
}

func main() {
	const mCases int64 = 8
	const nValues int64 = 16
	const kIters int64 = 1000000

	sets := make([][]Interval, mCases)
	for m := int64(0); m < mCases; m++ {
		sets[m] = buildCase(m*1000003+12345, nValues)
	}

	var sum int64 = 0
	for k := int64(0); k < kIters; k++ {
		idx := k % mCases
		r := mergeIntervals(sets[idx])
		sum += int64(len(r))
	}
	fmt.Println(sum)
}
