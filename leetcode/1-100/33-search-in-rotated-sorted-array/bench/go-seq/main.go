// LeetCode #33 bench — Go (mirror of search_rotated.kara).
//
// One-pass modified binary search over a fixed rotated-sorted array, TOTAL
// searches with cycling targets, folded into a checksum (single goroutine — seq).
package main

import "fmt"

func search(nums []int64, length, target int64) int64 {
	lo, hi := int64(0), length-1
	for lo <= hi {
		mid := lo + (hi-lo)/2
		m := nums[mid]
		if m == target {
			return mid
		}
		if nums[lo] <= m {
			if nums[lo] <= target && target < m {
				hi = mid - 1
			} else {
				lo = mid + 1
			}
		} else if m < target && target <= nums[hi] {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return -1
}

func main() {
	const n int64 = 4096
	const rot int64 = 1365
	const total int64 = 18000000
	const modulus int64 = 1000000007

	nums := make([]int64, 0, n)
	for p := int64(0); p < n; p++ {
		nums = append(nums, 2*((p+rot)%n))
	}

	span := 2 * n
	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		target := k % span
		idx := search(nums, n, target)
		acc = (acc + idx + 2) % modulus
	}

	fmt.Println(acc)
}
