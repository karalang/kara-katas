// benchmark's Go mirror of hills.kara (LeetCode #2210, the ★ arm): one
// pass keeping the last number that differs from the current one, a run
// counted once, at its end.
package main

import "fmt"

func countHillValley(nums []int64) int64 {
	var count int64
	left := nums[0]
	for i := 1; i < len(nums)-1; i++ {
		if nums[i] == nums[i+1] {
			continue
		}
		right := nums[i+1]
		if (nums[i] > left && nums[i] > right) || (nums[i] < left && nums[i] < right) {
			count++
		}
		if nums[i] != left {
			left = nums[i]
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2210)
	tops := []int64{3, 10, 100}
	arrays := [][]int64{}
	for a := 0; a < 2000; a++ {
		nums := make([]int64, 100)
		for i := range nums {
			nums[i] = nextRandom(&seed)%tops[a%3] + 1
		}
		arrays = append(arrays, nums)
	}
	// every array counted once per pass
	check := int64(0)
	for p := int64(0); p < 100; p++ {
		for _, nums := range arrays {
			check = (check*31 + countHillValley(nums) + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 2000 arrays: checksum %d\n", check)
}
