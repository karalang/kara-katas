// LeetCode #628: Maximum Product of Three Numbers -- Go mirror of the
// Kāra bench.
//
// The ★ arm's one pass over the same inputs and rounds.
package main

import (
	"fmt"
	"math"
)

func maximumProduct(nums []int64) int64 {
	max1, max2, max3 := int64(math.MinInt64), int64(math.MinInt64), int64(math.MinInt64)
	min1, min2 := int64(math.MaxInt64), int64(math.MaxInt64)
	for _, v := range nums {
		if v > max1 {
			max3 = max2
			max2 = max1
			max1 = v
		} else if v > max2 {
			max3 = max2
			max2 = v
		} else if v > max3 {
			max3 = v
		}
		if v < min1 {
			min2 = min1
			min1 = v
		} else if v < min2 {
			min2 = v
		}
	}
	top := max1 * max2 * max3
	ends := max1 * min1 * min2
	if top > ends {
		return top
	}
	return ends
}

var seed int64 = 628

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const inputs = 20
	const rounds = 20000
	all := make([][]int64, 0, inputs)
	for i := 0; i < inputs; i++ {
		spread := 1 + nextRandom()%1000
		nums := make([]int64, 0, 10000)
		for j := 0; j < 10000; j++ {
			nums = append(nums, nextRandom()%(2*spread+1)-spread)
		}
		all = append(all, nums)
	}
	var checksum int64
	for r := 0; r < rounds; r++ {
		p := maximumProduct(all[(r*7)%inputs])
		checksum = (checksum*31 + p%1000000007 + 1000000007) % 1000000007
	}
	fmt.Printf("%d inputs, %d rounds: checksum %d\n", inputs, rounds, checksum)
}
