// LeetCode #1498: Number of Subsequences That Satisfy the Given Sum
// Condition -- the bench in Go, mirroring num_subseq.kara: the values
// sorted, then two pointers.
package main

import (
	"fmt"
	"slices"
)

const mod = 1000000007

func numSubseq(nums []int32, target int32) int32 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	n := int64(len(sorted))
	pow2 := make([]int64, n)
	pow2[0] = 1
	for i := int64(1); i < n; i++ {
		pow2[i] = pow2[i-1] * 2 % mod
	}
	var count int64
	lo, hi := int64(0), n-1
	for lo <= hi {
		if sorted[lo]+sorted[hi] <= target {
			count = (count + pow2[hi-lo]) % mod
			lo++
		} else {
			hi--
		}
	}
	return int32(count)
}

func main() {
	var seed int64 = 1498
	nums := make([]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		nums = append(nums, int32(1+seed/65536*31%1000000))
	}
	var check int64
	for call := int64(0); call < 200; call++ {
		at := (check + call*7919) % 100000
		nums[at] = int32(1 + (check+call)%1000000)
		target := 1 + (check*13+call)%1000000
		check = (check*31 + int64(numSubseq(nums, int32(target)))) % 1000000007
	}
	fmt.Printf("200 calls over 100000 values: checksum %d\n", check)
}
