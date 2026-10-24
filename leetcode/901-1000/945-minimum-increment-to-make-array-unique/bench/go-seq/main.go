// Benchmark: LeetCode #945 Minimum Increment to Make Array Unique -- the
// ★ arm, sorted and raised, on arrays of 100000 values, LeetCode's
// longest. Mirrors min_increment_for_unique.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"slices"
)

func minIncrementForUnique(nums []int64) int64 {
	a := slices.Clone(nums)
	slices.Sort(a)
	var moves int64
	floor := int64(-1)
	for _, v := range a {
		end := max(v, floor+1)
		moves += end - v
		floor = end
	}
	return moves
}

var seed int64 = 945

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count, n := 5, 20, 100000
	arrays := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		rng := 70001 + nextRandom()*4%30001
		nums := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			wide := nextRandom() * 32768
			wide += nextRandom()
			nums = append(nums, wide%rng)
		}
		arrays = append(arrays, nums)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			m := minIncrementForUnique(arrays[(r+i)%count])
			total += m
			check = (check*1000003 + m) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d arrays of %d values: %d moves, checksum %d\n", rounds, count, n, total, check)
}
