// LeetCode #2765: Longest Alternating Subarray -- the bench
// (alternating.kara in Go): one pass with the length of the alternating
// run ending at each number.
package main

import "fmt"

var seed int64 = 2765

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func alternatingSubarray(nums []int64) int64 {
	best, run := int64(-1), int64(1)
	for i := 1; i < len(nums); i++ {
		if run >= 2 && nums[i] == nums[i-2] {
			run++
		} else if nums[i]-nums[i-1] == 1 {
			run = 2
		} else {
			run = 1
		}
		if run >= 2 && run > best {
			best = run
		}
	}
	return best
}

func main() {
	const count, rounds = 100000, 10
	cases := make([][]int64, count)
	for k := range cases {
		top := nextRandom()%4 + 2
		a := make([]int64, 100)
		for i := range a {
			a[i] = nextRandom()%top + 1
		}
		cases[k] = a
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range cases {
			length := alternatingSubarray(nums)
			sum += length
			check = (check*31 + length + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 100, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, sum, check)
}
