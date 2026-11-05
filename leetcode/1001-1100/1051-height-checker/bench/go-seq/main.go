// LeetCode #1051: Height Checker -- Go mirror of bench/height_checker.kara.
package main

import (
	"fmt"
	"slices"
)

var seed int64 = 1051

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func heightChecker(heights []int64) int64 {
	expected := slices.Clone(heights)
	slices.Sort(expected)
	var moved int64
	for i := range heights {
		if heights[i] != expected[i] {
			moved++
		}
	}
	return moved
}

func main() {
	lines, count, rounds := 2000, 100, 50
	all := make([][]int64, lines)
	for l := range all {
		all[l] = make([]int64, count)
		for i := range all[l] {
			all[l][i] = nextRandom()%100 + 1
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, heights := range all {
			answer := heightChecker(heights)
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("%d lines of %d students, %d rounds: total %d, checksum %d\n", lines, count, rounds, total, check)
}
