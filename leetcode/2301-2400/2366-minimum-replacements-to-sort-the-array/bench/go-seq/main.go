// LeetCode #2366: Minimum Replacements to Sort the Array -- the bench, the
// ★ arm in Go: greedy from the right, a value over the bound split into
// the fewest pieces that fit, the bound becoming the smallest piece of
// the most even split.
package main

import "fmt"

func minimumReplacement(nums []int64) int64 {
	n := len(nums)
	bound := nums[n-1]
	ops := int64(0)
	for i := n - 2; i >= 0; i-- {
		v := nums[i]
		if v <= bound {
			bound = v
		} else {
			k := (v + bound - 1) / bound
			ops += k - 1
			bound = v / k
		}
	}
	return ops
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// array a: 10^5 values from 1 to 10^(a - 1) when a > 0, and a falling
	// run from 10^9 when a is 0
	seed := int64(2366)
	arrays := make([][]int64, 0, 10)
	top := int64(1)
	for a := 0; a < 10; a++ {
		nums := make([]int64, 100000)
		for i := range nums {
			if a == 0 {
				nums[i] = 1000000000 - int64(i)*9999
			} else {
				hi := nextRandom(&seed)
				nums[i] = 1 + (hi*32768+nextRandom(&seed))%top
			}
		}
		arrays = append(arrays, nums)
		if a > 0 {
			top *= 10
		}
	}
	check := int64(0)
	for p := int64(0); p < 100; p++ {
		for _, nums := range arrays {
			check = (check*31 + minimumReplacement(nums)%1000000007 + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
