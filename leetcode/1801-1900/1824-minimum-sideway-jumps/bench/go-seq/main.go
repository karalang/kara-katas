// LeetCode #1824: Minimum Sideway Jumps -- the bench in Go: the ★ arm over
// 50 calls on roads of 250000 to 499999 steps cut from one road of
// 5 * 10^5 steps with an obstacle at half its points, built once, each
// road's length drawn from the checksum so far and its last point cleared.
package main

import (
	"fmt"
	"slices"
)

func minSideJumps(obstacles []int64) int64 {
	never := int64(len(obstacles)) + 1
	jumps := []int64{1, 0, 1}
	for i := 1; i < len(obstacles); i++ {
		if obstacles[i] > 0 {
			jumps[obstacles[i]-1] = never
		}
		best := slices.Min(jumps) + 1
		for lane := int64(0); lane < 3; lane++ {
			if obstacles[i] != lane+1 {
				jumps[lane] = min(jumps[lane], best)
			}
		}
	}
	return slices.Min(jumps)
}

var seed int64 = 1824

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	base := make([]int64, 500001)
	for i := 1; i < 500000; i++ {
		if nextRandom()%2 == 0 {
			base[i] = 1 + nextRandom()%3
		}
	}
	var check int64
	for call := int64(0); call < 50; call++ {
		n := 250000 + (check+call)%250000
		road := slices.Clone(base[:n+1])
		road[n] = 0
		check = (check*31 + minSideJumps(road)) % 1000000007
	}
	fmt.Printf("50 calls: checksum %d\n", check)
}
