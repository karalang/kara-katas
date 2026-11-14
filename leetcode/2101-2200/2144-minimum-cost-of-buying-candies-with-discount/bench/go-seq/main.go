// LeetCode #2144: Minimum Cost of Buying Candies With Discount -- the
// benchmark, the same algorithm as candies.kara.
package main

import (
	"fmt"
	"sort"
)

func minimumCost(cost []int64) int64 {
	dearestFirst := append([]int64(nil), cost...)
	sort.SliceStable(dearestFirst, func(i, j int) bool { return dearestFirst[i] > dearestFirst[j] })
	paid := int64(0)
	for i, c := range dearestFirst {
		if i%3 != 2 {
			paid += c
		}
	}
	return paid
}

var seed int64 = 2144

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	baskets := make([][]int64, 1000)
	for b := range baskets {
		baskets[b] = make([]int64, 100)
		for i := range baskets[b] {
			baskets[b][i] = nextRandom()%100 + 1
		}
	}
	total, check := int64(0), int64(0)
	for round := int64(0); round < 100; round++ {
		for b := 0; b < 1000; b++ {
			at := nextRandom() % 100
			baskets[b][at] = nextRandom()%100 + 1
			paid := minimumCost(baskets[b])
			total += paid
			check = (check*31 + paid + round) % 1000000007
		}
	}
	fmt.Printf("100000 solves: %d paid in all, checksum %d\n", total, check)
}
