// Benchmark for #493: Go mirror of the ★ arm (merge sort); see
// ../reverse_pairs.kara.
package main

import "fmt"

func sortCount(nums []int64, low, high int) int64 {
	if high-low <= 1 {
		return 0
	}
	mid := (low + high) / 2
	count := sortCount(nums, low, mid) + sortCount(nums, mid, high)
	j := mid
	for i := low; i < mid; i++ {
		for j < high && nums[i] > 2*nums[j] {
			j++
		}
		count += int64(j - mid)
	}
	var merged []int64
	a, b := low, mid
	for a < mid || b < high {
		if b == high || (a < mid && nums[a] <= nums[b]) {
			merged = append(merged, nums[a])
			a++
		} else {
			merged = append(merged, nums[b])
			b++
		}
	}
	copy(nums[low:], merged)
	return count
}

func reversePairs(nums []int64) int64 {
	work := append([]int64(nil), nums...)
	return sortCount(work, 0, len(work))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 60 arrays of 50,000 numbers across the whole 32-bit range, built
	// once, then each counted once.
	var arrays [][]int64
	var seed int64 = 493
	for k := 0; k < 60; k++ {
		nums := make([]int64, 0, 50000)
		for i := 0; i < 50000; i++ {
			high := nextRandom(&seed)
			nums = append(nums, high*131072+nextRandom(&seed)*4-2147483648)
		}
		arrays = append(arrays, nums)
	}
	var total, checksum int64
	for _, nums := range arrays {
		pairs := reversePairs(nums)
		total += pairs
		checksum = (checksum*31 + pairs) % 1000000007
	}
	fmt.Printf("60 arrays of 50000: %d reverse pairs, checksum %d\n", total, checksum)
}
