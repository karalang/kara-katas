// LeetCode #1356 bench -- Go: one sort keyed by the pair (the number of 1
// bits, the value), sort.Slice with a comparison.
package main

import (
	"fmt"
	"math/bits"
	"sort"
)

func sortByBits(arr []int32) []int32 {
	out := append([]int32(nil), arr...)
	sort.Slice(out, func(i, j int) bool {
		bi, bj := bits.OnesCount32(uint32(out[i])), bits.OnesCount32(uint32(out[j]))
		if bi != bj {
			return bi < bj
		}
		return out[i] < out[j]
	})
	return out
}

var seed int64 = 1356

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 arrays of 500 values from 0 to 10^4, the constraints' most, built
	// once; then 2 * 10^4 rounds, each setting one place of one array to a
	// value, all drawn from the checksum so far, sorting it, and folding
	// three values of the answer into the checksum
	arrays := make([][]int32, 20)
	for k := range arrays {
		arrays[k] = make([]int32, 500)
		for i := range arrays[k] {
			arrays[k][i] = int32(nextRandom() % 10001)
		}
	}
	var check int64
	for r := int64(0); r < 20000; r++ {
		k := check % 20
		arrays[k][(check/20)%500] = int32((check / 10000) % 10001)
		got := sortByBits(arrays[k])
		check = (check*31 + int64(got[0]) + int64(got[check%500])*7 + int64(got[499])*13 + r) % 1000000007
	}
	fmt.Printf("20000 rounds over 20 arrays of 500 values: checksum %d\n", check)
}
