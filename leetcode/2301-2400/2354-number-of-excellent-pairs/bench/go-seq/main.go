// LeetCode #2354: Number of Excellent Pairs -- the bench, the ★ arm in Go:
// the distinct values tallied by their count of set bits, then every two
// tallies whose bits reach k multiplied.
package main

import (
	"fmt"
	"math/bits"
)

func countExcellentPairs(nums []int64, k int64) int64 {
	distinct := make(map[int64]struct{})
	for _, x := range nums {
		distinct[x] = struct{}{}
	}
	var byBits [31]int64
	for x := range distinct {
		byBits[bits.OnesCount64(uint64(x))]++
	}
	total := int64(0)
	for a := 0; a < 31; a++ {
		for b := 0; b < 31; b++ {
			if int64(a+b) >= k {
				total += byBits[a] * byBits[b]
			}
		}
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// array a holds 10^5 values from 1 to 10^9, from 1 to 10^(4 + a / 2)
	// distinct; pass p asks for k = 1 + (7 p + a) mod 60
	seed := int64(2354)
	arrays := make([][]int64, 0, 10)
	spread := int64(10000)
	for a := 0; a < 10; a++ {
		nums := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			high := nextRandom(&seed)
			nums = append(nums, 1+(high*32768+nextRandom(&seed))%spread*99991%1000000000)
		}
		arrays = append(arrays, nums)
		if a%2 == 1 {
			spread *= 10
		}
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for a := int64(0); a < 10; a++ {
			k := 1 + (7*p+a)%60
			check = (check*31 + countExcellentPairs(arrays[a], k) + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
