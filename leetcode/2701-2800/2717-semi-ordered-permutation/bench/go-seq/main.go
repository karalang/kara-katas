// LeetCode #2717: Semi-Ordered Permutation -- the bench (semi.kara in
// Go): 1's index plus n's distance from the end, less one when 1 starts
// right of n, each index found by a scan.
package main

import "fmt"

func position(nums []int64, value int64) int64 {
	for i, v := range nums {
		if v == value {
			return int64(i)
		}
	}
	panic("missing")
}

func semiOrderedPermutation(nums []int64) int64 {
	n := int64(len(nums))
	first := position(nums, 1)
	last := position(nums, n)
	swaps := first + (n - 1 - last)
	if first > last {
		return swaps - 1
	}
	return swaps
}

var seed int64 = 2717

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 200000, 20
	perms := make([][]int64, 0, count)
	for k := 0; k < count; k++ {
		nums := make([]int64, 50)
		for i := range nums {
			nums[i] = int64(i + 1)
		}
		for i := int64(49); i >= 1; i-- {
			j := nextRandom() % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		perms = append(perms, nums)
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, nums := range perms {
			swaps := semiOrderedPermutation(nums)
			sum += swaps
			check = (check*31 + swaps + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d permutations of 50, %d rounds: swaps sum to %d, checksum %d\n", count, rounds, sum, check)
}
