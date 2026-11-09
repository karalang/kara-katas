// LeetCode #2044: Count Number of Maximum Bitwise-OR Subsets -- the ★ arm
// in Go, the same algorithm and workload as subsets.kara: the target is the
// OR of every value, and a take-or-skip search counts the subsets that
// reach it.
package main

import "fmt"

func countFrom(nums []int64, i int, acc, target int64) int64 {
	if i == len(nums) {
		if acc == target {
			return 1
		}
		return 0
	}
	return countFrom(nums, i+1, acc|nums[i], target) + countFrom(nums, i+1, acc, target)
}

func countMaxOrSubsets(nums []int64) int64 {
	var target int64
	for _, x := range nums {
		target |= x
	}
	return countFrom(nums, 0, 0, target)
}

var seed int64 = 2044

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	tops := []int64{100000, 1024, 16, 2}
	arrays := make([][]int64, 2000)
	for r := range arrays {
		arrays[r] = make([]int64, 16)
		for i := range arrays[r] {
			arrays[r][i] = nextRandom()%tops[r%4] + 1
		}
	}
	var calls, sum, check int64
	for _, nums := range arrays {
		answer := countMaxOrSubsets(nums)
		calls++
		sum += answer
		check = (check*31 + answer) % 1000000007
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
