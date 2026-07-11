// Benchmark workload — Search in Rotated Sorted Array II (LeetCode #81).
// Go mirror of ../search_rotated_ii.kara. Build-once + punch: one rotated sorted
// array with duplicates (each value 0..M appears twice, M=1000, rotated) built once,
// then searched K=17,000,000 times for targets sweeping present/absent values, each
// boolean folded through a rolling polynomial hash. The duplicate-aware rotated
// binary search's branch loop is the measured work.
package main

import "fmt"

func search(nums []int64, length, target int64) bool {
	lo, hi := int64(0), length-1
	for lo <= hi {
		mid := lo + (hi-lo)/2
		if nums[mid] == target {
			return true
		}
		if nums[lo] == nums[mid] && nums[mid] == nums[hi] {
			lo++
			hi--
		} else if nums[lo] <= nums[mid] {
			if nums[lo] <= target && target < nums[mid] {
				hi = mid - 1
			} else {
				lo = mid + 1
			}
		} else {
			if nums[mid] < target && target <= nums[hi] {
				lo = mid + 1
			} else {
				hi = mid - 1
			}
		}
	}
	return false
}

func build(m, dup, rot int64) []int64 {
	n := m * dup
	base := make([]int64, 0, n)
	for v := int64(0); v < m; v++ {
		for d := int64(0); d < dup; d++ {
			base = append(base, v)
		}
	}
	arr := make([]int64, n)
	for i := int64(0); i < n; i++ {
		arr[i] = base[(i+rot)%n]
	}
	return arr
}

func main() {
	const m = 1000
	const dup = 2
	const total = 17000000
	const modulus = 1000000007
	arr := build(m, dup, (m*dup)/3)
	n := int64(len(arr))
	span := int64(m + 50)
	var sum int64 = 0
	for iter := int64(0); iter < total; iter++ {
		target := iter % span
		found := search(arr, n, target)
		var bit int64 = 0
		if found {
			bit = 1
		}
		sum = (sum*131 + bit + 1) % modulus
	}
	fmt.Println(sum)
}
