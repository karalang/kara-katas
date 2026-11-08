// LeetCode #2012: Sum of Beauty in the Array -- the ★ arm's benchmark, a
// mirror of beauty.kara.
package main

import "fmt"

func sumOfBeauties(nums []int64) int64 {
	n := len(nums)
	minAfter := make([]int64, n)
	minAfter[n-1] = nums[n-1]
	for i := n - 2; i >= 0; i-- {
		minAfter[i] = min(minAfter[i+1], nums[i])
	}
	maxBefore := nums[0]
	var total int64
	for i := 1; i < n-1; i++ {
		if maxBefore < nums[i] && nums[i] < minAfter[i+1] {
			total += 2
		} else if nums[i-1] < nums[i] && nums[i] < nums[i+1] {
			total++
		}
		maxBefore = max(maxBefore, nums[i])
	}
	return total
}

var seed int64 = 2012

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 1000)
	for a := int64(0); a < 1000; a++ {
		rise := a % 11
		nums := make([]int64, 0, 2000)
		for i := 0; i < 2000; i++ {
			if i > 0 && nextRandom()%10 < rise {
				nums = append(nums, min(nums[i-1]+nextRandom()%3+1, 100000))
			} else {
				nums = append(nums, nextRandom()%100000+1)
			}
		}
		arrays = append(arrays, nums)
	}
	var calls, sum, check int64
	for r := 0; r < 5; r++ {
		for _, nums := range arrays {
			answer := sumOfBeauties(nums)
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
