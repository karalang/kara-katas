// Benchmark: LeetCode #977 Squares of a Sorted Array -- the ★ arm, two
// pointers from the ends, on 20 sorted arrays of 10000 numbers. Mirrors
// sorted_squares.kara, .rs, .c and .py.
package main

import (
	"fmt"
	"slices"
)

func sortedSquares(nums []int64) []int64 {
	n := len(nums)
	out := make([]int64, n)
	lo, hi, at := 0, n-1, n-1
	for lo <= hi {
		a := nums[lo] * nums[lo]
		b := nums[hi] * nums[hi]
		if a > b {
			out[at] = a
			lo++
		} else {
			out[at] = b
			hi--
		}
		at--
	}
	return out
}

var seed int64 = 977

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count, n := 500, 20, 10000
	arrays := make([][]int64, count)
	for c := range arrays {
		arrays[c] = make([]int64, n)
		for i := range arrays[c] {
			arrays[c][i] = nextRandom()%20001 - 10000
		}
		slices.Sort(arrays[c])
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			out := sortedSquares(arrays[(r+i)%count])
			total += out[0] + out[n-1]
			check = (check*31 + out[(r*13+i*7)%n]) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d arrays of 10000 numbers: squares total %d, checksum %d\n", rounds, count, total, check)
}
