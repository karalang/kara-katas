// LeetCode #1365 bench -- Go: the values counted and the counts summed, so
// below[v] holds how many values are less than v.
package main

import "fmt"

func smallerNumbersThanCurrent(nums []int32) []int32 {
	var below [102]int32
	for _, x := range nums {
		below[x+1]++
	}
	for v := 1; v < 102; v++ {
		below[v] += below[v-1]
	}
	out := make([]int32, len(nums))
	for i, x := range nums {
		out[i] = below[x]
	}
	return out
}

var seed int64 = 1365

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 arrays of 500 values from 0 to 100, the constraints' most, built
	// once; then 2 * 10^5 rounds, each setting one value of one array, both
	// drawn from the checksum so far, and folding three of the answers
	// into the checksum
	arrays := make([][]int32, 20)
	for k := range arrays {
		arrays[k] = make([]int32, 500)
		for i := range arrays[k] {
			arrays[k][i] = int32(nextRandom() % 101)
		}
	}
	var check int64
	for r := int64(0); r < 200000; r++ {
		k := check % 20
		arrays[k][(check/20)%500] = int32((check / 10000) % 101)
		got := smallerNumbersThanCurrent(arrays[k])
		check = (check*31 + int64(got[0]) + int64(got[check%500])*7 + int64(got[499])*13 + r) % 1000000007
	}
	fmt.Printf("200000 rounds over 20 arrays of 500 values: checksum %d\n", check)
}
