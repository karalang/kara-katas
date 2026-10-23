// LeetCode #875 bench: Go mirror of min_eating_speed.kara (the ★ arm,
// binary search on the speed) on the same 600 searches.
package main

import "fmt"

func minEatingSpeed(piles []int64, h int64) int64 {
	lo, hi := int64(1), int64(1)
	for _, p := range piles {
		if p > hi {
			hi = p
		}
	}
	for lo < hi {
		k := (lo + hi) / 2
		if hours(piles, k) <= h {
			hi = k
		} else {
			lo = k + 1
		}
	}
	return lo
}

func hours(piles []int64, k int64) int64 {
	var total int64
	for _, p := range piles {
		total += (p + k - 1) / k
	}
	return total
}

var seed int64 = 875

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func upTo(limit int64) int64 {
	a := nextRandom()
	b := nextRandom()
	return (a*32768+b)%limit + 1
}

func main() {
	pileSets := make([][]int64, 0, 20)
	for k := 0; k < 20; k++ {
		limit := int64(1000000)
		if k%2 == 0 {
			limit = 1000000000
		}
		piles := make([]int64, 10000)
		for i := range piles {
			piles[i] = upTo(limit)
		}
		pileSets = append(pileSets, piles)
	}
	var total, check int64
	for k := 0; k < 600; k++ {
		span := int64(1000000)
		if k%3 == 0 {
			span = 1000000000 - 10000
		}
		h := 10000 + upTo(span) - 1
		answer := minEatingSpeed(pileSets[k%20], h)
		total += answer
		check = (check*131 + answer) % 1000000007
	}
	fmt.Printf("600 searches over 10000 piles: speeds sum to %d, checksum %d\n", total, check)
}
