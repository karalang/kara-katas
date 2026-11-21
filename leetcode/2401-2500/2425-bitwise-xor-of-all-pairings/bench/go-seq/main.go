// LeetCode #2425: Bitwise XOR of All Pairings -- the bench, the ★ arm: the
// XOR of `nums1` when `nums2` has odd length, XORed with that of `nums2`
// when `nums1` has odd length.
package main

import "fmt"

func xorAllNums(nums1, nums2 []int64) int64 {
	var answer int64
	if len(nums2)%2 == 1 {
		for _, x := range nums1 {
			answer ^= x
		}
	}
	if len(nums1)%2 == 1 {
		for _, y := range nums2 {
			answer ^= y
		}
	}
	return answer
}

var seed int64 = 2425

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var firsts, seconds [][]int64
	for i := int64(0); i < 10; i++ {
		for which := 0; which < 2; which++ {
			n := 100000 - i
			if which == 1 {
				n = 100000 - i/2 - 1
			}
			nums := make([]int64, 0, n)
			for k := int64(0); k < n; k++ {
				a := nextRandom()
				nums = append(nums, (a*32768+nextRandom())%1000000001)
			}
			if which == 0 {
				firsts = append(firsts, nums)
			} else {
				seconds = append(seconds, nums)
			}
		}
	}
	var check int64
	for p := int64(0); p < 500; p++ {
		for i := 0; i < 10; i++ {
			at := (p * 7919) % int64(len(firsts[i]))
			firsts[i][at] ^= p % 1024
			check = (check*31 + xorAllNums(firsts[i], seconds[i]) + p) % 1000000007
		}
	}
	fmt.Printf("500 passes over 10 pairs of 10^5 values: checksum %d\n", check)
}
