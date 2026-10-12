// Benchmark for #435: mirror of erase_overlap.kara (greedy by end) on
// 100 windows of 100,000 intervals from one pool of 1,000,000. The sort
// is not stable; the count does not depend on the order of intervals
// with equal ends.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type interval struct{ start, end int64 }

func eraseOverlapIntervals(intervals []interval) int64 {
	if len(intervals) == 0 {
		return 0
	}
	slices.SortFunc(intervals, func(a, b interval) int { return cmp.Compare(a.end, b.end) })
	kept := int64(1)
	end := intervals[0].end
	for i := 1; i < len(intervals); i++ {
		if intervals[i].start >= end {
			kept++
			end = intervals[i].end
		}
	}
	return int64(len(intervals)) - kept
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const poolSize, size, rounds int64 = 1000000, 100000, 100
	seed := int64(435)
	// Starts anywhere in [-50000, 50000), lengths 1 to 200.
	pool := make([]interval, 0, poolSize)
	for i := int64(0); i < poolSize; i++ {
		hi := nextRandom(&seed)
		start := (hi*32768+nextRandom(&seed))%100000 - 50000
		pool = append(pool, interval{start, start + 1 + nextRandom(&seed)%200})
	}
	var total, checksum int64
	for r := int64(0); r < rounds; r++ {
		at := nextRandom(&seed) * 32768 % (poolSize - size + 1)
		window := make([]interval, 0)
		for i := at; i < at+size; i++ {
			window = append(window, pool[i])
		}
		removed := eraseOverlapIntervals(window)
		total += removed
		checksum = (checksum*31 + removed) % 1000000007
	}
	fmt.Printf("%d rounds of %d intervals: %d removed, checksum %d\n", rounds, size, total, checksum)
}
