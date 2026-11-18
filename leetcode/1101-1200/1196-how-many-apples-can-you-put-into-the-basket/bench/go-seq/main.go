// LeetCode #1196 bench: the ★ arm in Go, over the same 200 baskets of
// 10^3 apples and 200 rounds as the Kāra bench; each call copies its
// basket and sorts the copy with `slices.Sort`.
package main

import (
	"fmt"
	"slices"
)

func maxNumberOfApples(basket []int64) int64 {
	weight := slices.Clone(basket)
	slices.Sort(weight)
	var load int64
	for i, w := range weight {
		load += w
		if load > 5000 {
			return int64(i)
		}
	}
	return int64(len(weight))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	lows := []int64{1, 1, 300, 1}
	highs := []int64{1000, 20, 1000, 100}
	seed := int64(1196)
	baskets := make([][]int64, 0, 200)
	for k := 0; k < 200; k++ {
		low, high := lows[k%4], highs[k%4]
		basket := make([]int64, 1000)
		for j := range basket {
			basket[j] = low + nextRandom(&seed)%(high-low+1)
		}
		baskets = append(baskets, basket)
	}
	var check int64
	for r := 0; r < 200; r++ {
		for _, basket := range baskets {
			apples := maxNumberOfApples(basket)
			check = (check*131 + apples + 1) % 1000000007
		}
	}
	fmt.Printf("200 rounds of 200 baskets of 1000 apples: checksum %d\n", check)
}
