// Benchmark for #436: mirror of right_interval.kara (sorted starts and
// binary search) on 100 random sets of 20,000 intervals. The index sort
// is not stable; starts are distinct, so the order is the same.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type interval struct{ start, end int64 }

func findRightInterval(intervals []interval) []int64 {
	n := len(intervals)
	order := make([]int, n)
	for i := range order {
		order[i] = i
	}
	slices.SortFunc(order, func(a, b int) int { return cmp.Compare(intervals[a].start, intervals[b].start) })
	right := make([]int64, 0, n)
	for i := 0; i < n; i++ {
		end := intervals[i].end
		lo, hi := 0, n
		for lo < hi {
			mid := (lo + hi) / 2
			if intervals[order[mid]].start < end {
				lo = mid + 1
			} else {
				hi = mid
			}
		}
		if lo < n {
			right = append(right, int64(order[lo]))
		} else {
			right = append(right, -1)
		}
	}
	return right
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const size, rounds int64 = 20000, 100
	seed := int64(436)
	var found, checksum int64
	for r := int64(0); r < rounds; r++ {
		// Distinct starts, one in each step of 100 across the range,
		// each interval up to 32,767 long, then shuffled.
		intervals := make([]interval, 0, size)
		for i := int64(0); i < size; i++ {
			start := -1000000 + 100*i + nextRandom(&seed)%100
			end := min(start+nextRandom(&seed), 1000000)
			intervals = append(intervals, interval{start, end})
		}
		for i := int64(0); i < size; i++ {
			j := i + nextRandom(&seed)%(size-i)
			intervals[i], intervals[j] = intervals[j], intervals[i]
		}
		for _, j := range findRightInterval(intervals) {
			if j >= 0 {
				found++
			}
			checksum = (checksum*31 + j + 2) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d intervals: %d right intervals, checksum %d\n", rounds, size, found, checksum)
}
