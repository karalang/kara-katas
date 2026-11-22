// LeetCode #2790: Maximum Number of Groups With Increasing Length -- the
// bench in Go: the ★ arm over 20 arrays of 10^5 limits up to 10^9, all
// drawn first, then each answered 10 times, each answer sorting its own
// copy.
package main

import (
	"fmt"
	"slices"
)

func maxIncreasingGroups(usageLimits []int64) int64 {
	limits := slices.Clone(usageLimits)
	slices.Sort(limits)
	var groups, places int64
	for _, u := range limits {
		places += u
		if places >= (groups+1)*(groups+2)/2 {
			groups++
		}
	}
	return groups
}

var seed int64 = 2790

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
	for c := 0; c < count; c++ {
		var top int64 = 1000000000
		if c%2 == 1 {
			top = 100000
		}
		cases[c] = make([]int64, 100000)
		for i := range cases[c] {
			cases[c][i] = wide()%top + 1
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := maxIncreasingGroups(cases[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 10^5, %d rounds: groups sum to %d, checksum %d\n", count, rounds, total, check)
}
