package main

import "fmt"

func findMin(nums []int64, n int64) int64 {
	var lo int64 = 0
	hi := n - 1
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] > nums[hi] {
			lo = mid + 1
		} else if nums[mid] < nums[hi] {
			hi = mid
		} else {
			hi = hi - 1
		}
	}
	return nums[lo]
}

func main() {
	var n, punches int64 = 2000, 75000
	arr := make([]int64, n)

	var state int64 = 12345
	var sink int64 = 0
	for pn := int64(0); pn < punches; pn++ {
		state = (state*1103515245 + 12345) & 2147483647
		start := state % 1000000
		state = (state*1103515245 + 12345) & 2147483647
		rot := state % n

		cur := start
		for k := int64(0); k < n; k++ {
			state = (state*1103515245 + 12345) & 2147483647
			var inc int64
			if state%5 == 0 {
				inc = (state / 5) % 4
			} else {
				inc = 0
			}
			cur += inc
			arr[(k+rot)%n] = cur
		}

		sink += findMin(arr, n)
	}
	fmt.Println(sink)
}
