// LeetCode #57 — Go goroutine-parallel mirror (par lane, insert_interval).
// Same linear three-phase insert; the K=1M reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
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

// Count-only insert — the par lane skips materializing the output.
func insertInterval(intervals []interval, newStart, newEnd int64) int64 {
	var count int64 = 0
	n := len(intervals)
	i := 0
	for i < n && intervals[i].end < newStart {
		count++
		i++
	}
	for i < n && intervals[i].start <= newEnd {
		if intervals[i].start < newStart {
			newStart = intervals[i].start
		}
		if intervals[i].end > newEnd {
			newEnd = intervals[i].end
		}
		i++
	}
	count++
	for i < n {
		count++
		i++
	}
	return count
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
func lcgNext(state int64) int64 {
	return (1103515245*state + 12345) % 2147483648
}

func buildCase(seed, count int64) []interval {
	v := make([]interval, 0, count)
	state := seed
	var cursor int64 = 0
	for j := int64(0); j < count; j++ {
		state = lcgNext(state)
		gap := (state % 4) + 2
		state = lcgNext(state)
		width := (state % 6) + 1
		start := cursor + gap
		end := start + width
		v = append(v, interval{start: start, end: end})
		cursor = end
	}
	return v
}

func pickNew(c []interval, m, count int64) (int64, int64) {
	half := count / 2
	st := lcgNext(m*7919 + 101)
	lo := st % half
	st = lcgNext(st)
	span := st % half
	hi := lo + 1 + span
	if hi > count-1 {
		hi = count - 1
	}
	return c[lo].start, c[hi].end
}

func main() {
	sets := make([][]interval, mCases)
	newStart := make([]int64, mCases)
	newEnd := make([]int64, mCases)
	for m := int64(0); m < mCases; m++ {
		sets[m] = buildCase(m*1000003+12345, nValues)
		newStart[m], newEnd[m] = pickNew(sets[m], m, nValues)
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
				s += insertInterval(sets[idx], newStart[idx], newEnd[idx])
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
