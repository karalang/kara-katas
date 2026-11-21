// LeetCode #2465: Number of Distinct Averages -- the bench, the ★ arm in
// Go: a sorted copy, the `i`th smallest paired with the `i`th largest,
// and the pairs' sums put in a `map`.
package main

import (
	"fmt"
	"slices"
)

func distinctAverages(nums []int64) int64 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	n := len(sorted)
	sums := map[int64]bool{}
	for i := 0; i < n/2; i++ {
		sums[sorted[i]+sorted[n-1-i]] = true
	}
	return int64(len(sums))
}

var seed int64 = 2465

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 1000 lists of 100 numbers from 0 to 100 built once; then 900
	// passes, each setting one number of every list from the checksum so
	// far, then answering every list and folding the answer plus the pass
	// into the checksum
	lists := make([][]int64, 1000)
	for a := range lists {
		lists[a] = make([]int64, 100)
		for i := range lists[a] {
			lists[a][i] = nextRandom() % 101
		}
	}
	check := int64(0)
	for p := int64(0); p < 900; p++ {
		for a := range lists {
			lists[a][(check+int64(a))%100] = check % 101
			check = (check*31 + distinctAverages(lists[a]) + p) % 1000000007
		}
	}
	fmt.Printf("900 passes over 1000 lists of 100: checksum %d\n", check)
}
