// LeetCode #2348: Number of Zero-Filled Subarrays -- the bench, the ★ arm
// in Go: the length of the run of zeros ending at each place, summed.
package main

import "fmt"

func zeroFilledSubarray(nums []int64) int64 {
	run, total := int64(0), int64(0)
	for _, x := range nums {
		if x == 0 {
			run++
		} else {
			run = 0
		}
		total += run
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// array a holds a value that is not zero with a chance of 1 in a + 2
	seed := int64(2348)
	arrays := make([][]int64, 10)
	for a := int64(0); a < 10; a++ {
		arrays[a] = make([]int64, 100000)
		for i := range arrays[a] {
			r := nextRandom(&seed)
			if r%(a+2) == 0 {
				arrays[a][i] = r + 1
			}
		}
	}
	check := int64(0)
	for p := int64(0); p < 60; p++ {
		for _, nums := range arrays {
			check = (check*31 + zeroFilledSubarray(nums) + p) % 1000000007
		}
	}
	fmt.Printf("60 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
