// LeetCode #2104: Sum of Subarray Ranges -- bench, Go mirror of
// ranges.kara.
package main

import "fmt"

func subArrayRanges(nums []int64, stack []int) int64 {
	n := len(nums)
	var sum int64
	stack = stack[:0]
	for i := 0; i <= n; i++ {
		for len(stack) > 0 && (i == n || nums[stack[len(stack)-1]] < nums[i]) {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			left := -1
			if len(stack) > 0 {
				left = stack[len(stack)-1]
			}
			sum += nums[top] * int64(top-left) * int64(i-top)
		}
		stack = append(stack, i)
	}
	stack = stack[:0]
	for i := 0; i <= n; i++ {
		for len(stack) > 0 && (i == n || nums[stack[len(stack)-1]] > nums[i]) {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			left := -1
			if len(stack) > 0 {
				left = stack[len(stack)-1]
			}
			sum -= nums[top] * int64(top-left) * int64(i-top)
		}
		stack = append(stack, i)
	}
	return sum
}

var seed int64 = 2104

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	arrays := make([][]int64, 1000)
	for a := range arrays {
		arrays[a] = make([]int64, 1000)
		for k := range arrays[a] {
			arrays[a][k] = wideRandom()%2000000001 - 1000000000
		}
	}
	stack := make([]int, 0, 1001)
	var total, check int64
	for p := 0; p < 10; p++ {
		for _, nums := range arrays {
			got := subArrayRanges(nums, stack) % 1000000007
			total = (total + got) % 1000000007
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("10000 arrays: total %d, checksum %d\n", total, check)
}
