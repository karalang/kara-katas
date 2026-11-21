// LeetCode #2460: Apply Operations to an Array -- the bench, the ★ arm in
// Go: the operations in place, then the nonzero values moved forward by a
// write index and the rest filled with zeros.
package main

import "fmt"

func applyOperations(nums []int64) []int64 {
	n := len(nums)
	for i := 0; i < n-1; i++ {
		if nums[i] == nums[i+1] {
			nums[i] *= 2
			nums[i+1] = 0
		}
	}
	k := 0
	for i := 0; i < n; i++ {
		if nums[i] != 0 {
			nums[k] = nums[i]
			k++
		}
	}
	for i := k; i < n; i++ {
		nums[i] = 0
	}
	return nums
}

var seed int64 = 2460

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 1000 arrays of 2000 values from 0 to 3 built once; then 24 passes,
	// each setting one value of every array from the checksum so far,
	// then answering every array on a copy and folding every value of
	// the answer, plus the pass, into the checksum
	arrays := make([][]int64, 1000)
	for a := range arrays {
		arrays[a] = make([]int64, 2000)
		for i := range arrays[a] {
			arrays[a][i] = nextRandom() % 4
		}
	}
	check := int64(0)
	for p := int64(0); p < 24; p++ {
		for a := range arrays {
			arrays[a][(check+int64(a))%2000] = check % 4
			for _, v := range applyOperations(append([]int64(nil), arrays[a]...)) {
				check = (check*31 + v + p) % 1000000007
			}
		}
	}
	fmt.Printf("24 passes over 1000 arrays of 2000: checksum %d\n", check)
}
