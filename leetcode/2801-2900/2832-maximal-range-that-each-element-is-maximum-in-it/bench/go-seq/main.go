// LeetCode #2832: Maximal Range That Each Element Is Maximum in It --
// the bench, mirrored from ranges.kara: two passes of a falling stack.
package main

import "fmt"

func maximumLengthOfRanges(nums []int64) []int64 {
	n := len(nums)
	left := make([]int64, n)
	right := make([]int64, n)
	stack := make([]int, 0)
	for i := 0; i < n; i++ {
		for len(stack) > 0 && nums[stack[len(stack)-1]] <= nums[i] {
			stack = stack[:len(stack)-1]
		}
		left[i] = -1
		if len(stack) > 0 {
			left[i] = int64(stack[len(stack)-1])
		}
		stack = append(stack, i)
	}
	stack = stack[:0]
	for i := n - 1; i >= 0; i-- {
		for len(stack) > 0 && nums[stack[len(stack)-1]] <= nums[i] {
			stack = stack[:len(stack)-1]
		}
		right[i] = int64(n)
		if len(stack) > 0 {
			right[i] = int64(stack[len(stack)-1])
		}
		stack = append(stack, i)
	}
	ans := make([]int64, n)
	for i := range ans {
		ans[i] = right[i] - left[i] - 1
	}
	return ans
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 20, 20, 100000
	seed := int64(2832)
	arrays := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = int64(i + 1)
		}
		for i := int64(n - 1); i >= 1; i-- {
			hi := nextRandom(&seed)
			j := (hi*32768 + nextRandom(&seed)) % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		arrays = append(arrays, nums)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			for _, x := range maximumLengthOfRanges(nums) {
				total += x
				check = (check*31 + x + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: ranges total %d, checksum %d\n", count, n, rounds, total, check)
}
