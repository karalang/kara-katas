// Benchmark for #487: Go mirror of the ★ arm (the run before the
// last 0); see ../max_consecutive_ones_ii.kara.
package main

import "fmt"

func findMaxConsecutiveOnes(nums []int64) int64 {
	var best, before, run int64
	for _, x := range nums {
		if x == 1 {
			run++
		} else {
			before = run + 1
			run = 0
		}
		if before+run > best {
			best = before + run
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	arrays := [][]int64{}
	var seed int64 = 487
	for a := int64(0); a < 20; a++ {
		nums := []int64{}
		for i := 0; i < 100000; i++ {
			if nextRandom(&seed)%100 < 80+a {
				nums = append(nums, 1)
			} else {
				nums = append(nums, 0)
			}
		}
		arrays = append(arrays, nums)
	}
	var total, checksum int64
	for r := 0; r < 50; r++ {
		for _, nums := range arrays {
			best := findMaxConsecutiveOnes(nums)
			total += best
			checksum = (checksum*31 + best) % 1000000007
		}
	}
	fmt.Printf("1000 scans of 100000 numbers: runs add up to %d, checksum %d\n", total, checksum)
}
