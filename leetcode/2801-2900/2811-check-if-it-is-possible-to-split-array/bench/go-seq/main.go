// LeetCode #2811: Check if it is Possible to Split Array -- the bench in
// Go: the ★ arm over 100000 arrays of 100 numbers up to 100, m from 150
// to 200, all drawn first, then each answered 10 times.
package main

import "fmt"

func canSplitArray(nums []int64, m int64) bool {
	if len(nums) <= 2 {
		return true
	}
	for i := 1; i < len(nums); i++ {
		if nums[i-1]+nums[i] >= m {
			return true
		}
	}
	return false
}

var seed int64 = 2811

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 100000
	rounds := 10
	nums := make([][]int64, count)
	ms := make([]int64, count)
	for c := range nums {
		nums[c] = make([]int64, 100)
		for i := range nums[c] {
			nums[c][i] = nextRandom()%100 + 1
		}
		ms[c] = 150 + nextRandom()%51
	}
	var yes, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := range nums {
			var a int64
			if canSplitArray(nums[c], ms[c]) {
				a = 1
			}
			yes += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 100, %d rounds: %d can split, checksum %d\n", count, rounds, yes, check)
}
