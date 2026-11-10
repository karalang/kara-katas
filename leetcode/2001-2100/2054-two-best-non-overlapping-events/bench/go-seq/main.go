// LeetCode #2054: Two Best Non-Overlapping Events -- Go mirror of the ★
// arm's benchmark (two.kara): the same 50 sets of 100000 events, the same
// sort by (start, end, value), best value from each event on, and binary
// search for each event's first later start.
package main

import (
	"fmt"
	"slices"
	"sort"
)

var seed int64 = 2054

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

type event struct{ start, end, value int64 }

func maxTwoEvents(given []event) int64 {
	events := slices.Clone(given)
	slices.SortStableFunc(events, func(a, b event) int {
		switch {
		case a.start != b.start:
			if a.start < b.start {
				return -1
			}
			return 1
		case a.end != b.end:
			if a.end < b.end {
				return -1
			}
			return 1
		case a.value < b.value:
			return -1
		case a.value > b.value:
			return 1
		}
		return 0
	})
	n := len(events)
	bestFrom := make([]int64, n+1)
	for i := n - 1; i >= 0; i-- {
		bestFrom[i] = max(bestFrom[i+1], events[i].value)
	}
	var best int64
	for _, e := range events {
		next := sort.Search(n, func(j int) bool { return events[j].start > e.end })
		best = max(best, e.value+bestFrom[next])
	}
	return best
}

func main() {
	longests := []int64{1000, 1000000, 100000000, 500000000}
	var total, check int64
	for t := 0; t < 50; t++ {
		longest := longests[t%4]
		span := 1000000000 - longest
		events := make([]event, 0, 100000)
		for i := 0; i < 100000; i++ {
			start := wide()%span + 1
			end := start + wide()%longest
			value := wide()%1000000 + 1
			events = append(events, event{start, end, value})
		}
		best := maxTwoEvents(events)
		total += best
		check = (check*31 + best) % 1000000007
	}
	fmt.Printf("50 sets: sum %d, checksum %d\n", total, check)
}
