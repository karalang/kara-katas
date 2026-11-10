// Benchmark: LeetCode #1099 Two Sum Less Than K -- Go mirror of
// two_sum_less_than_k.kara: the ★ arm, sorting and two pointers, over 64
// arrays of 100 values built once, 400 rounds each changing one value per
// array and asking for 8 values of k.
package main

import (
	"fmt"
	"sort"
)

func twoSumLessThanK(nums []int64, k int64) int64 {
	v := make([]int64, len(nums))
	copy(v, nums)
	sort.Slice(v, func(a, b int) bool { return v[a] < v[b] })
	best := int64(-1)
	lo, hi := 0, len(v)-1
	for lo < hi {
		sum := v[lo] + v[hi]
		if sum < k {
			if sum > best {
				best = sum
			}
			lo++
		} else {
			hi--
		}
	}
	return best
}

var seed int64 = 1099

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 64)
	for j := range arrays {
		arrays[j] = make([]int64, 100)
		for i := range arrays[j] {
			arrays[j][i] = nextRandom()%1000 + 1
		}
	}
	var found, check int64
	for round := int64(0); round < 400; round++ {
		for j := int64(0); j < 64; j++ {
			at := (round*7 + j*13) % 100
			arrays[j][at] = (arrays[j][at]+round*31)%1000 + 1
			for q := int64(0); q < 8; q++ {
				k := (round*97+j*61+q*251)%2000 + 1
				best := twoSumLessThanK(arrays[j], k)
				if best >= 0 {
					found++
				}
				check = (check*31 + best + 1) % 1000000007
			}
		}
	}
	fmt.Printf("400 rounds over 64 arrays of 100 values: %d of 204800 with a pair, checksum %d\n", found, check)
}
