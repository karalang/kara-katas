// Benchmark for #525: Go mirror of the ★ arm (first index of each
// balance); see ../find_max_length.kara. A built-in map, a fresh one for
// every call.
package main

import "fmt"

func findMaxLength(nums []int64) int64 {
	first := map[int64]int64{0: -1}
	balance, best := int64(0), int64(0)
	for i := int64(0); i < int64(len(nums)); i++ {
		if nums[i] == 1 {
			balance++
		} else {
			balance--
		}
		if j, ok := first[balance]; ok {
			if i-j > best {
				best = i - j
			}
		} else {
			first[balance] = i
		}
	}
	return best
}

var seed int64 = 525

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := [][]int64{}
	for a := int64(0); a < 20; a++ {
		q := 2 + a%3
		nums := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			if nextRandom()%q == 0 {
				nums = append(nums, 1)
			} else {
				nums = append(nums, 0)
			}
		}
		arrays = append(arrays, nums)
	}
	total, checksum := int64(0), int64(0)
	for r := 0; r < 20; r++ {
		for a := range arrays {
			answer := findMaxLength(arrays[a])
			total += answer
			checksum = (checksum*31 + answer) % 1000000007
		}
	}
	fmt.Printf("20 arrays of 100000, 20 rounds: total %d, checksum %d\n", total, checksum)
}
