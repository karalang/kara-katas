// LeetCode #1751: Maximum Number of Events That Can Be Attended II -- the
// bench (events.kara in Go): sorted by end, one layer of k at a time.
package main

import (
	"fmt"
	"sort"
)

func maxValue(given [][]int32, k int32) int32 {
	events := make([][]int32, len(given))
	copy(events, given)
	sort.SliceStable(events, func(a, b int) bool { return events[a][1] < events[b][1] })
	n := len(events)
	ends := make([]int32, n)
	for i, e := range events {
		ends[i] = e[1]
	}
	before := make([]int, n)
	for i, e := range events {
		start := e[0]
		before[i] = sort.Search(n, func(j int) bool { return ends[j] >= start })
	}
	previous := make([]int32, n+1)
	for layer := int32(0); layer < k; layer++ {
		current := make([]int32, n+1)
		for i := 0; i < n; i++ {
			current[i+1] = max(current[i], previous[before[i]]+events[i][2])
		}
		previous = current
	}
	return previous[n]
}

var seed int64 = 1751

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	const count, rounds, n, k = 10, 5, 100000, 10
	problems := make([][][]int32, count)
	for c := range problems {
		problems[c] = make([][]int32, n)
		for i := range problems[c] {
			start := wide()%1000000000 + 1
			end := min(start+wide()%100000000, 1000000000)
			value := wide()%1000000 + 1
			problems[c][i] = []int32{int32(start), int32(end), int32(value)}
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, events := range problems {
			answer := int64(maxValue(events, k))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d events, k = %d, %d rounds: values add to %d, checksum %d\n", count, n, k, rounds, sum, check)
}
