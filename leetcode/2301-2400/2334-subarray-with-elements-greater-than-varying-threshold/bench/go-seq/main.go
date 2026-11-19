// LeetCode #2334: Subarray With Elements Greater Than Varying Threshold --
// the bench, the ★ arm in Go: the nearest smaller element on either side
// from a monotonic stack, and the widest run whose least element times
// its width exceeds the threshold.
package main

import "fmt"

func validSubarraySize(nums []int64, threshold int64) int64 {
	n := int64(len(nums))
	left := make([]int64, n)
	right := make([]int64, n)
	for i := range left {
		left[i] = -1
		right[i] = n
	}
	stack := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		for len(stack) > 0 && nums[stack[len(stack)-1]] >= nums[i] {
			right[stack[len(stack)-1]] = i
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			left[i] = stack[len(stack)-1]
		}
		stack = append(stack, i)
	}
	best := int64(-1)
	for i := int64(0); i < n; i++ {
		width := right[i] - left[i] - 1
		if nums[i]*width > threshold && width > best {
			best = width
		}
	}
	return best
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	arrays := make([][]int64, 10)
	for a := int64(0); a < 10; a++ {
		arrays[a] = make([]int64, 100000)
		for i := int64(0); i < 100000; i++ {
			arrays[a][i] = scrambled(a*100000+i)%1000000000 + 1
		}
	}
	var check int64
	for p := int64(0); p < 5; p++ {
		for a := int64(0); a < 10; a++ {
			threshold := ((10*a+p)*7919%1000 + 1) * 1000000
			check = (check*31 + validSubarraySize(arrays[a], threshold) + 1) % 1000000007
		}
	}
	fmt.Printf("5 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
