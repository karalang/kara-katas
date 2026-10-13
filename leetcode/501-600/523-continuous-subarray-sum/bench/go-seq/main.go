// Benchmark for #523: Go mirror of the ★ arm (first index of each prefix
// remainder); see ../check_subarray_sum.kara. A built-in map, a fresh one
// for every call.
package main

import "fmt"

func checkSubarraySum(nums []int64, k int64) bool {
	first := map[int64]int64{0: -1}
	var rem int64
	for i := int64(0); i < int64(len(nums)); i++ {
		rem = (rem + nums[i]) % k
		if j, ok := first[rem]; ok {
			if i-j >= 2 {
				return true
			}
		} else {
			first[rem] = i
		}
	}
	return false
}

var seed int64 = 523

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 random arrays of 100,000 numbers from 1 to 20,000 (the
	// problem's longest, summing under 2^31) made once; then each checked
	// in 10 rounds against a fresh k from 10,000 to 1,073,751,823.
	arrays := make([][]int64, 20)
	for a := range arrays {
		arrays[a] = make([]int64, 100000)
		for i := range arrays[a] {
			arrays[a][i] = 1 + nextRandom()%20000
		}
	}
	var yes, checksum int64
	for round := int64(0); round < 10; round++ {
		for a := range arrays {
			high := nextRandom()
			k := 10000 + high*32768 + nextRandom()
			if checkSubarraySum(arrays[a], k) {
				yes++
				checksum = (checksum + (round+1)*(int64(a)+1)) % 1000000007
			}
		}
	}
	fmt.Printf("20 arrays of 100000, 10 rounds: %d true, checksum %d\n", yes, checksum)
}
