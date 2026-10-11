// Benchmark for #376 -- mirror of wiggle.kara.
package main

import "fmt"

func wiggleMaxLength(nums []int64) int64 {
	if len(nums) == 0 {
		return 0
	}
	var up, down int64 = 1, 1
	for i := 1; i < len(nums); i++ {
		if nums[i] > nums[i-1] {
			up = down + 1
		} else if nums[i] < nums[i-1] {
			down = up + 1
		}
	}
	if up > down {
		return up
	}
	return down
}

func main() {
	var seed, checksum int64 = 376, 0
	nums := make([]int64, 1000)
	for c := 0; c < 20000; c++ {
		var top int64 = 1001
		if c%3 == 0 {
			top = 6
		}
		for i := range nums {
			seed = (seed*1103515245 + 12345) % 2147483648
			nums[i] = (seed / 65536) % top
		}
		checksum = (checksum*1009 + wiggleMaxLength(nums)) % 1000000007
	}
	fmt.Printf("checksum %d\n", checksum)
}
