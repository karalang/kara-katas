// Benchmark workload — Insert Interval (LeetCode #57).
// Go mirror of ../insert_interval.kara. Same M/N/K, LCG generator,
// cursor-based disjoint-sorted case builder, per-case new interval, linear
// three-phase insert, and sink — see that file's header for the rationale.

package main

import "fmt"

type Interval struct {
	Start int64
	End   int64
}

func insertInterval(intervals []Interval, newStart, newEnd int64) []Interval {
	result := make([]Interval, 0, len(intervals)+1)
	n := len(intervals)
	i := 0

	// Phase 1 — intervals entirely left of the new one.
	for i < n && intervals[i].End < newStart {
		result = append(result, intervals[i])
		i++
	}
	// Phase 2 — absorb every overlapping/touching interval.
	for i < n && intervals[i].Start <= newEnd {
		if intervals[i].Start < newStart {
			newStart = intervals[i].Start
		}
		if intervals[i].End > newEnd {
			newEnd = intervals[i].End
		}
		i++
	}
	result = append(result, Interval{newStart, newEnd})
	// Phase 3 — the untouched tail.
	for i < n {
		result = append(result, intervals[i])
		i++
	}
	return result
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
func lcgNext(state int64) int64 {
	return (1103515245*state + 12345) % 2147483648
}

func buildCase(seed, count int64) []Interval {
	v := make([]Interval, 0, count)
	state := seed
	var cursor int64 = 0
	for j := int64(0); j < count; j++ {
		state = lcgNext(state)
		gap := (state % 4) + 2
		state = lcgNext(state)
		width := (state % 6) + 1
		start := cursor + gap
		end := start + width
		v = append(v, Interval{start, end})
		cursor = end
	}
	return v
}

func pickNew(c []Interval, m, count int64) (int64, int64) {
	half := count / 2
	st := lcgNext(m*7919 + 101)
	lo := st % half
	st = lcgNext(st)
	span := st % half
	hi := lo + 1 + span
	if hi > count-1 {
		hi = count - 1
	}
	return c[lo].Start, c[hi].End
}

func main() {
	const mCases int64 = 8
	const nValues int64 = 16
	const kIters int64 = 1000000

	sets := make([][]Interval, mCases)
	newStart := make([]int64, mCases)
	newEnd := make([]int64, mCases)
	for m := int64(0); m < mCases; m++ {
		sets[m] = buildCase(m*1000003+12345, nValues)
		newStart[m], newEnd[m] = pickNew(sets[m], m, nValues)
	}

	var sum int64 = 0
	for k := int64(0); k < kIters; k++ {
		idx := k % mCases
		r := insertInterval(sets[idx], newStart[idx], newEnd[idx])
		sum += int64(len(r))
	}
	fmt.Println(sum)
}
