// LeetCode #2779: Maximum Beauty of an Array After Applying Operation --
// the bench in Go: the ★ arm over 20 arrays of 10^5 numbers, all drawn
// first, then each answered 10 times, every answer sorting its own copy.
package main

import (
	"fmt"
	"slices"
)

func maximumBeauty(nums []int64, k int64) int64 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	var best, lo int64
	for hi := int64(0); hi < int64(len(sorted)); hi++ {
		for sorted[hi]-sorted[lo] > 2*k {
			lo++
		}
		best = max(best, hi-lo+1)
	}
	return best
}

var seed int64 = 2779

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count := 20
	rounds := 10
	cases := make([][]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		cases[c] = make([]int64, 100000)
		for i := range cases[c] {
			cases[c][i] = wide() % 100001
		}
		ks[c] = wide() % 1001
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			b := maximumBeauty(cases[c], ks[c])
			total += b
			check = (check*31 + b + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 10^5, %d rounds: beauties sum to %d, checksum %d\n", count, rounds, total, check)
}
