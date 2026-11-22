// LeetCode #2824: Count Pairs Whose Sum is Less than Target -- the
// bench's Go mirror of the ★ arm: the numbers sorted, two pointers
// closing in.
package main

import (
	"fmt"
	"slices"
)

func countPairs(nums []int64, target int64) int64 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	i, j := 0, len(sorted)-1
	var count int64
	for i < j {
		if sorted[i]+sorted[j] < target {
			count += int64(j - i)
			i++
		} else {
			j--
		}
	}
	return count
}

var seed int64 = 2824

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 200000, 5
	nums := make([][]int64, count)
	targets := make([]int64, count)
	for c := 0; c < count; c++ {
		nums[c] = make([]int64, 50)
		for i := range nums[c] {
			nums[c][i] = nextRandom()%101 - 50
		}
		targets[c] = nextRandom()%101 - 50
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < count; c++ {
			a := countPairs(nums[c], targets[c])
			total += a
			check = (check*31 + a + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 50, %d rounds: %d pairs, checksum %d\n", count, rounds, total, check)
}
