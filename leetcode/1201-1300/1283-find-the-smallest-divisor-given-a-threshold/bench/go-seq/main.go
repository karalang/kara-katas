// LeetCode #1283 bench, Go: the same binary search, workload and
// checksum as smallest_divisor.kara.
package main

import "fmt"

func total(nums []int32, d int64) int64 {
	var sum int64
	for _, x := range nums {
		sum += (int64(x) + d - 1) / d
	}
	return sum
}

func smallestDivisor(nums []int32, threshold int32) int32 {
	var lo int64 = 1
	hi := int64(nums[0])
	for _, x := range nums {
		if int64(x) > hi {
			hi = int64(x)
		}
	}
	for lo < hi {
		mid := (lo + hi) / 2
		if total(nums, mid) <= int64(threshold) {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return int32(lo)
}

func main() {
	var seed int64 = 1283
	nums := make([]int32, 0, 50000)
	for i := 0; i < 50000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		nums = append(nums, int32(1+seed%1000000))
	}
	var check int64
	for r := int64(0); r < 150; r++ {
		threshold := 50000 + (check+r*7919)%950001
		check = (check*131 + int64(smallestDivisor(nums, int32(threshold)))) % 1000000007
	}
	fmt.Printf("150 rounds over 5 * 10^4 numbers: checksum %d\n", check)
}
