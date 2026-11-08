// LeetCode #1509: Minimum Difference Between Largest and Smallest Value in
// Three Moves -- the bench: 20 arrays of 100000 numbers built once, then
// each answered five times by the ★ arm.
package main

import (
	"fmt"
	"slices"
)

func minDifference(nums []int64) int64 {
	n := len(nums)
	if n <= 4 {
		return 0
	}
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	best := sorted[n-1] - sorted[0]
	for low := 0; low < 4; low++ {
		best = min(best, sorted[n-4+low]-sorted[low])
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1509)
	arrays := make([][]int64, 20)
	for a := range arrays {
		arrays[a] = make([]int64, 100000)
		for i := range arrays[a] {
			wide := nextRandom(&seed) * 32768
			wide += nextRandom(&seed)
			arrays[a][i] = wide%2000000001 - 1000000000
		}
	}
	var check int64
	for r := 0; r < 5; r++ {
		for _, nums := range arrays {
			check = (check*31 + minDifference(nums)%1000000007 + 1) % 1000000007
		}
	}
	fmt.Printf("100 answers over 20 arrays of 100000 numbers: checksum %d\n", check)
}
