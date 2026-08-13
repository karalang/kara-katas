// Benchmark workload for LeetCode #259 — 3Sum Smaller (Go mirror).
// Mirrors three_sum_smaller.kara algorithm-for-algorithm.
package main

import (
	"fmt"
	"sort"
)

func main() {
	var n int64 = 4000
	var rounds int64 = 26

	base := make([]int64, n)
	var state int64 = 259259
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		base[i] = (state/65536)%2001 - 1000
	}
	probe := make([]int64, n)
	copy(probe, base)
	sort.Slice(probe, func(a, b int) bool { return probe[a] < probe[b] })
	minSum := probe[0] + probe[1] + probe[2]
	maxSum := probe[n-1] + probe[n-2] + probe[n-3]
	target := (minSum + maxSum) / 2

	s := make([]int64, n)
	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		copy(s, base)
		sort.Slice(s, func(a, b int) bool { return s[a] < s[b] })
		var count int64 = 0
		for a := int64(0); a+2 < n; a++ {
			lo, hi := a+1, n-1
			for lo < hi {
				if s[a]+s[lo]+s[hi] < target {
					count += hi - lo
					lo++
				} else {
					hi--
				}
			}
		}
		sink = (sink*31 + count%1000000007) % 1000000007
	}
	fmt.Println(sink)
}
