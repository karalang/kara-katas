// Benchmark for #360 -- mirror of sort_transformed.kara.
package main

import "fmt"

func f(x, a, b, c int64) int64 {
	return a*x*x + b*x + c
}

func sortTransformedArray(nums []int64, a, b, c int64) []int64 {
	n := int64(len(nums))
	out := make([]int64, n)
	lo, hi := int64(0), n-1
	if a >= 0 {
		k := n - 1
		for lo <= hi {
			left, right := f(nums[lo], a, b, c), f(nums[hi], a, b, c)
			if left >= right {
				out[k] = left
				lo++
			} else {
				out[k] = right
				hi--
			}
			k--
		}
	} else {
		k := int64(0)
		for lo <= hi {
			left, right := f(nums[lo], a, b, c), f(nums[hi], a, b, c)
			if left <= right {
				out[k] = left
				lo++
			} else {
				out[k] = right
				hi--
			}
			k++
		}
	}
	return out
}

func main() {
	var seed int64 = 360
	var checksum int64
	nums := make([]int64, 50000)
	for round := 0; round < 200; round++ {
		x := int64(-1000000)
		for i := range nums {
			seed = (seed*1103515245 + 12345) % 2147483648
			x += (seed / 65536) % 81
			nums[i] = x
		}
		seed = (seed*1103515245 + 12345) % 2147483648
		a := (seed/65536)%21 - 10
		seed = (seed*1103515245 + 12345) % 2147483648
		b := (seed/65536)%21 - 10
		seed = (seed*1103515245 + 12345) % 2147483648
		c := (seed/65536)%21 - 10
		for _, v := range sortTransformedArray(nums, a, b, c) {
			checksum = (checksum*31 + v%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
