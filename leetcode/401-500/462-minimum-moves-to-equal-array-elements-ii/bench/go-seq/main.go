// Benchmark for #462: mirror of min_moves2.kara (the ★ arm: sort, take
// the median) on the same workload. The sort is slices.Sort.
package main

import (
	"fmt"
	"slices"
)

func minMoves2(nums []int64) int64 {
	sorted := nums
	slices.Sort(sorted)
	median := sorted[len(sorted)/2]
	moves := int64(0)
	for _, x := range sorted {
		d := x - median
		if d < 0 {
			d = -d
		}
		moves += d
	}
	return moves
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomNumber(seed *int64) int64 {
	const spread = 1000000000
	a := nextRandom(seed)
	b := nextRandom(seed)
	c := nextRandom(seed)
	return ((a*32768+b)*32768+c)%(2*spread+1) - spread
}

func main() {
	const n int64 = 1000000
	const rounds = 10
	seed := int64(462)
	nums := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		nums = append(nums, randomNumber(&seed))
	}
	total := int64(0)
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		hi := nextRandom(&seed)
		lo := nextRandom(&seed)
		k := (hi*65536 + lo) % n
		nums[k] = randomNumber(&seed)
		moves := minMoves2(slices.Clone(nums))
		total += moves
		checksum = (checksum*31 + moves%1000003) % 1000000007
	}
	fmt.Printf("%d rounds on %d numbers: %d moves in all, checksum %d\n", rounds, n, total, checksum)
}
