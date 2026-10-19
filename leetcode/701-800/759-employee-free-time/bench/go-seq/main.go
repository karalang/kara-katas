// LeetCode 759 — Employee Free Time: benchmark, the ★ arm in Go.
package main

import (
	"fmt"
	"sort"
)

type Interval struct {
	start, end int64
}

func employeeFreeTime(schedule [][]Interval) []Interval {
	all := []Interval{}
	for _, employee := range schedule {
		all = append(all, employee...)
	}
	sort.Slice(all, func(i, j int) bool { return all[i].start < all[j].start })
	free := []Interval{}
	end := all[0].end
	for _, interval := range all {
		if interval.start > end {
			free = append(free, Interval{end, interval.start})
		}
		if interval.end > end {
			end = interval.end
		}
	}
	return free
}

var seed int64 = 759

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	rounds := 3000
	gaps := int64(0)
	length := int64(0)
	check := int64(0)
	for r := 0; r < rounds; r++ {
		schedule := [][]Interval{}
		for e := 0; e < 50; e++ {
			employee := []Interval{}
			t := int64(0)
			for i := 0; i < 50; i++ {
				start := t + wideRandom()%1000000
				end := start + 1 + wideRandom()%900000
				employee = append(employee, Interval{start, end})
				t = end + 1
			}
			schedule = append(schedule, employee)
		}
		free := employeeFreeTime(schedule)
		gaps += int64(len(free))
		for _, interval := range free {
			length += interval.end - interval.start
			check = (check*31 + interval.start) % 1000000007
		}
	}
	fmt.Printf("%d schedules of 50 x 50 intervals: %d free intervals, %d free in all, checksum %d\n", rounds, gaps, length, check)
}
