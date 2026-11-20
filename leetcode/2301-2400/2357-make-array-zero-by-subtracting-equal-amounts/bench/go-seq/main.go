// LeetCode #2357: Make Array Zero by Subtracting Equal Amounts -- the
// bench, the ★ arm in Go: the distinct positive values gathered in a map
// used as a set.
package main

import "fmt"

func minimumOperations(nums []int64) int64 {
	seen := make(map[int64]struct{})
	for _, x := range nums {
		if x > 0 {
			seen[x] = struct{}{}
		}
	}
	return int64(len(seen))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 2 * 10^4 arrays of 100 values from 0 to 1 up to 0 to 100
	seed := int64(2357)
	arrays := make([][]int64, 0, 20000)
	for a := 0; a < 20000; a++ {
		top := 2 + nextRandom(&seed)%100
		nums := make([]int64, 100)
		for i := range nums {
			nums[i] = nextRandom(&seed) % top
		}
		arrays = append(arrays, nums)
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for _, nums := range arrays {
			check = (check*31 + minimumOperations(nums) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 2 * 10^4 arrays of 100 values: checksum %d\n", check)
}
