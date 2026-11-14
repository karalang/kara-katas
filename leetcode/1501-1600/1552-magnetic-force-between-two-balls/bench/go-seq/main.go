// LeetCode #1552: Magnetic Force Between Two Balls -- bench: the ★ arm (a
// binary search on the answer, a greedy check) over 20 baskets of 100000
// distinct positions up to 10^9, built once, each asked 5 times with its own
// number of balls every time. Go mirror of magnetic.kara.
package main

import (
	"fmt"
	"slices"
)

func fits(sorted []int64, m, gap int64) bool {
	placed := int64(1)
	last := sorted[0]
	for _, p := range sorted {
		if p-last >= gap {
			placed++
			last = p
		}
	}
	return placed >= m
}

func maxDistance(position []int64, m int64) int64 {
	sorted := slices.Clone(position)
	slices.Sort(sorted)
	lo, hi := int64(1), sorted[len(sorted)-1]-sorted[0]
	for lo < hi {
		mid := lo + (hi-lo+1)/2
		if fits(sorted, m, mid) {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return lo
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	seed := int64(1552)
	baskets := [][]int64{}
	for b := 0; b < 20; b++ {
		taken := map[int64]bool{}
		position := []int64{}
		for len(position) < 100000 {
			p := (nextRandom(&seed)*32768+nextRandom(&seed))%1000000000 + 1
			if !taken[p] {
				taken[p] = true
				position = append(position, p)
			}
		}
		baskets = append(baskets, position)
	}
	check := int64(0)
	for pass := int64(0); pass < 5; pass++ {
		for b := range baskets {
			m := (pass*20+int64(b))*997%99999 + 2
			check = mix(check, maxDistance(baskets[b], m))
		}
	}
	fmt.Printf("5 passes over 20 baskets of 100000 positions: checksum %d\n", check)
}
