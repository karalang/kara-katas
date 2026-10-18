// LeetCode #704 bench: the ★ arm in Go. See the .kara twin for the
// workload.
package main

import "fmt"

func search(nums []int64, target int64) int64 {
	lo := int64(0)
	hi := int64(len(nums)) - 1
	for lo <= hi {
		mid := lo + (hi-lo)/2
		if nums[mid] == target {
			return mid
		}
		if nums[mid] < target {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(704)
	arrays := make([][]int64, 0, 100)
	for a := 0; a < 100; a++ {
		nums := make([]int64, 0)
		v := int64(-9999)
		for i := 0; i < 10000; i++ {
			nums = append(nums, v)
			v += 1 + nextRandom(&seed)%2
		}
		arrays = append(arrays, nums)
	}
	found := int64(0)
	checksum := int64(0)
	for round := 0; round < 5; round++ {
		for _, nums := range arrays {
			for target := int64(-9999); target < 10000; target++ {
				at := search(nums, target)
				if at >= 0 {
					found++
				}
				checksum = (checksum*31 + at + 1) % 1000000007
			}
		}
	}
	fmt.Printf("5 rounds of 100 arrays of 10000: %d found, checksum %d\n", found, checksum)
}
