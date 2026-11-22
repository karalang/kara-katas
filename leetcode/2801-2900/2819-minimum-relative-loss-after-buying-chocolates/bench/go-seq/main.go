// LeetCode #2819: Minimum Relative Loss After Buying Chocolates -- the
// bench's Go mirror of the ★ arm: the prices sorted, prefix sums, and a
// binary search per query for how many come from the cheap end.
package main

import (
	"fmt"
	"slices"
)

func minimumRelativeLosses(prices []int64, queries [][2]int64) []int64 {
	sorted := slices.Clone(prices)
	slices.Sort(sorted)
	n := int64(len(sorted))
	prefix := make([]int64, n+1)
	for i := int64(0); i < n; i++ {
		prefix[i+1] = prefix[i] + sorted[i]
	}
	out := make([]int64, 0, len(queries))
	for _, q := range queries {
		k, m := q[0], q[1]
		lo, hi := int64(0), m
		for lo < hi {
			mid := (lo + hi) / 2
			if sorted[mid]+sorted[n-m+mid] < 2*k {
				lo = mid + 1
			} else {
				hi = mid
			}
		}
		dear := prefix[n] - prefix[n-m+lo]
		out = append(out, prefix[lo]+2*k*(m-lo)-dear)
	}
	return out
}

var seed int64 = 2819

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count, rounds, n := 10, 3, int64(100000)
	prices := make([][]int64, count)
	queries := make([][][2]int64, count)
	for c := 0; c < count; c++ {
		prices[c] = make([]int64, n)
		for i := range prices[c] {
			prices[c][i] = wide()%1000000000 + 1
		}
		queries[c] = make([][2]int64, n)
		for i := range queries[c] {
			k := wide()%1000000000 + 1
			queries[c][i] = [2]int64{k, wide()%n + 1}
		}
	}
	var negative, check int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < count; c++ {
			for _, a := range minimumRelativeLosses(prices[c], queries[c]) {
				if a < 0 {
					negative++
				}
				check = ((check*31+a+int64(r))%1000000007 + 1000000007) % 1000000007
			}
		}
	}
	fmt.Printf("%d shops of %d, %d rounds: %d losses below 0, checksum %d\n", count, n, rounds, negative, check)
}
